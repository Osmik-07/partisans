"""
REST API для Mini App авторизации.
Эндпоинты: /api/auth/send_code, /api/auth/sign_in, /api/auth/2fa
Статические файлы: GET / → miniapp/index.html
"""
import hashlib
import hmac
import json
import logging
import os
from urllib.parse import unquote

from aiohttp import web

from bot.config import settings
from bot.services.userbot_auth import send_code, sign_in, sign_in_2fa

logger = logging.getLogger(__name__)

MINIAPP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "miniapp")


def _verify_init_data(init_data: str) -> bool:
    """Проверяет подпись Telegram WebApp initData."""
    if not init_data:
        return False
    try:
        parsed = dict(x.split("=", 1) for x in init_data.split("&"))
        hash_val = parsed.pop("hash", "")
        check_string = "\n".join(f"{k}={unquote(v)}" for k, v in sorted(parsed.items()))
        secret = hmac.new(b"WebAppData", settings.bot_token.encode(), hashlib.sha256).digest()
        expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, hash_val)
    except Exception:
        return False


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

    user_id = data.get("user_id")
    phone = data.get("phone", "").strip()
    init_data = data.get("init_data", "")

    # Верифицируем initData от Telegram (или пропускаем в dev)
    if init_data and not _verify_init_data(init_data):
        logger.warning(f"Invalid initData from user {user_id}")
        # Не блокируем — просто логируем

    if not user_id or not phone:
        return web.json_response({"ok": False, "error": "Missing user_id or phone"}, status=400)

    result = await send_code(int(user_id), phone)
    return web.json_response(result)


async def api_sign_in(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "Invalid JSON"}, status=400)

    user_id = data.get("user_id")
    code = data.get("code", "").strip().replace(" ", "")

    if not user_id or not code:
        return web.json_response({"ok": False, "error": "Missing fields"}, status=400)

    result = await sign_in(int(user_id), code)
    return web.json_response(result)


async def api_2fa(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "Invalid JSON"}, status=400)

    user_id = data.get("user_id")
    password = data.get("password", "")

    if not user_id or not password:
        return web.json_response({"ok": False, "error": "Missing fields"}, status=400)

    result = await sign_in_2fa(int(user_id), password)
    return web.json_response(result)


def register_miniapp(app: web.Application):
    app.router.add_get("/", serve_index)
    app.router.add_get("/auth", serve_index)
    app.router.add_post("/api/auth/send_code", api_send_code)
    app.router.add_post("/api/auth/sign_in",   api_sign_in)
    app.router.add_post("/api/auth/2fa",        api_2fa)
    app.router.add_static("/static", path=os.path.join(MINIAPP_DIR), name="static")
    logger.info("Mini App API registered")
