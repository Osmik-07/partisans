import json

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Telegram Bot
    bot_token: str
    # Хранится как строка, т.к. pydantic-settings пытается распарсить list[int]
    # из env как JSON и падает на простом "123456789" (валидный JSON-int, но не список).
    # Поддерживаем оба формата: "123456789", "111,222" и "[111, 222]".
    admin_ids_raw: str = Field(default="", validation_alias="ADMIN_IDS")

    # Pyrogram (MTProto)
    telegram_api_id: int = 0
    telegram_api_hash: str = ""
    userbot_session_secret: str = ""

    # Mini App
    miniapp_domain: str = "traceapp.ru"  # твой домен

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "notspybot"
    db_user: str = "notspybot"
    db_pass: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # CryptoBot
    cryptobot_token: str = ""
    cryptobot_webhook_secret: str = ""

    # Webhook / Mini App server
    webhook_host: str = ""
    webhook_path: str = "/webhook"
    webhook_port: int = 8443

    # Prices USD
    price_trial_days: int = 3
    price_week_usd: float = 1.00
    price_month_usd: float = 2.00
    price_year_usd: float = 10.00

    # Prices Stars
    price_week_stars: int = 50
    price_month_stars: int = 100
    price_year_stars: int = 500

    # Protection (разовый продукт «Защита от перехвата»)
    price_protection_usd: float = 100.00
    price_protection_stars: int = 5000

    # Referral program
    referral_bonus_days: int = 1
    referral_stars_percent: int = 25

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def use_webhook(self) -> bool:
        return bool(self.webhook_host)

    @property
    def admin_ids(self) -> list[int]:
        raw = self.admin_ids_raw.strip()
        if not raw:
            return []
        if raw.startswith("["):
            return [int(x) for x in json.loads(raw)]
        return [int(x.strip()) for x in raw.split(",") if x.strip()]


settings = Settings()
