"""
REST API для Mini App авторизации.
Эндпоинты: /api/auth/send_code, /api/auth/sign_in, /api/auth/2fa
Статические файлы: GET / → miniapp/index.html
"""
import logging
import os

from aiohttp import web

from bot.config import settings
from bot.services.security import get_init_data_user_id
from bot.services.subscription import user_has_active_subscription
from bot.services.userbot_auth import send_code, sign_in, sign_in_2fa

logger = logging.getLogger(__name__)

MINIAPP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "miniapp")

async def _get_authorized_user_id(request: web.Request, data: dict) -> int | None:
    init_data = data.get("init_data", "")
    user_id = get_init_data_user_id(init_data)
    if not user_id:
        return None

    async with request.app["db_sessionmaker"]() as session:
        if not await user_has_active_subscription(session, user_id):
            raise web.HTTPForbidden(
                text='{"ok": false, "error": "Active subscription required"}',
                content_type="application/json",
            )

    return user_id


async def serve_index(request: web.Request) -> web.Response:
    """Отдаёт Mini App HTML страницу."""
    index_path = os.path.join(MINIAPP_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    return web.Response(text=content, content_type="text/html")


async def api_send_code(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "Invalid JSON"}, status=400)

    phone = data.get("phone", "").strip()
    user_id = await _get_authorized_user_id(request, data)
    if not user_id:
        return web.json_response({"ok": False, "error": "Invalid Telegram session"}, status=401)

    if not phone:
        return web.json_response({"ok": False, "error": "Missing phone"}, status=400)

    result = await send_code(user_id, phone)
    return web.json_response(result)


async def api_sign_in(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "Invalid JSON"}, status=400)

    code = data.get("code", "").strip().replace(" ", "")
    user_id = await _get_authorized_user_id(request, data)
    if not user_id:
        return web.json_response({"ok": False, "error": "Invalid Telegram session"}, status=401)

    if not code:
        return web.json_response({"ok": False, "error": "Missing code"}, status=400)

    result = await sign_in(user_id, code)
    return web.json_response(result)


async def api_2fa(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "Invalid JSON"}, status=400)

    password = data.get("password", "")
    user_id = await _get_authorized_user_id(request, data)
    if not user_id:
        return web.json_response({"ok": False, "error": "Invalid Telegram session"}, status=401)

    if not password:
        return web.json_response({"ok": False, "error": "Missing password"}, status=400)

    result = await sign_in_2fa(user_id, password)
    return web.json_response(result)


def register_miniapp(app: web.Application):
    app.router.add_get("/", serve_index)
    app.router.add_get("/auth", serve_index)
    app.router.add_post("/api/auth/send_code", api_send_code)
    app.router.add_post("/api/auth/sign_in",   api_sign_in)
    app.router.add_post("/api/auth/2fa",        api_2fa)
    app.router.add_static("/static", path=os.path.join(MINIAPP_DIR), name="static")
    logger.info("Mini App API registered")
