import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from urllib.parse import parse_qsl

from cryptography.fernet import Fernet, InvalidToken

from bot.config import settings

INIT_DATA_TTL_SECONDS = 6 * 60 * 60


def _build_webapp_secret() -> bytes:
    return hmac.new(b"WebAppData", settings.bot_token.encode(), hashlib.sha256).digest()


def parse_init_data(init_data: str) -> dict | None:
    if not init_data:
        return None

    try:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        hash_value = parsed.pop("hash", "")
        if not hash_value:
            return None

        check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        expected = hmac.new(
            _build_webapp_secret(),
            check_string.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, hash_value):
            return None

        auth_date_raw = parsed.get("auth_date")
        if auth_date_raw:
            auth_date = datetime.fromtimestamp(int(auth_date_raw), tz=timezone.utc)
            age = (datetime.now(timezone.utc) - auth_date).total_seconds()
            if age < -60 or age > INIT_DATA_TTL_SECONDS:
                return None

        if parsed.get("user"):
            parsed["user"] = json.loads(parsed["user"])

        return parsed
    except Exception:
        return None


def get_init_data_user_id(init_data: str) -> int | None:
    parsed = parse_init_data(init_data)
    if not parsed:
        return None

    user = parsed.get("user")
    if not isinstance(user, dict) or "id" not in user:
        return None

    try:
        return int(user["id"])
    except (TypeError, ValueError):
        return None


def _build_fernet() -> Fernet:
    secret = settings.userbot_session_secret or settings.bot_token
    digest = hashlib.sha256(secret.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_session_string(session_string: str) -> str:
    return _build_fernet().encrypt(session_string.encode()).decode()


def decrypt_session_string(session_string: str) -> str:
    try:
        return _build_fernet().decrypt(session_string.encode()).decode()
    except InvalidToken:
        # Совместимость со старыми незашифрованными записями.
        return session_string
