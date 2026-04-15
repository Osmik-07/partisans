from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config import settings
from bot.i18n import t, LANGUAGES


def main_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t("btn_buy", lang),     callback_data="sub:plans")
    b.button(text=t("btn_status", lang),  callback_data="sub:status")
    b.button(text=t("btn_connect", lang), callback_data="help:connect")
    b.button(text=t("btn_userbot", lang), callback_data="userbot:menu")
    b.button(text=t("btn_language", lang),callback_data="lang:menu")
    b.adjust(1)
    return b.as_markup()


def plans_kb(lang: str = "en", trial_available: bool = False) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if trial_available:
        b.button(text=t("btn_trial", lang), callback_data="buy:trial")
    b.button(text=f"⚡️ 7 {_days(lang)} — ${settings.price_week_usd}",  callback_data="buy:week")
    b.button(text=f"🔥 30 {_days(lang)} — ${settings.price_month_usd}", callback_data="buy:month")
    b.button(text=f"👑 1 {_year(lang)} — ${settings.price_year_usd}",   callback_data="buy:year")
    b.button(text=t("btn_back", lang), callback_data="back:main")
    b.adjust(1)
    return b.as_markup()


def payment_method_kb(lang: str, plan: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="💎 CryptoBot (USDT/TON/BTC)", callback_data=f"pay:crypto:{plan}")
    b.button(text="⭐️ Telegram Stars",           callback_data=f"pay:stars:{plan}")
    b.button(text=t("btn_back", lang),            callback_data="sub:plans")
    b.adjust(1)
    return b.as_markup()


def pay_crypto_kb(lang: str, pay_url: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="💳 Pay", url=pay_url)
    b.button(text="✅ " + ("Я оплатил" if lang == "ru" else "I paid"), callback_data="pay:check")
    b.button(text=t("btn_back", lang), callback_data="sub:plans")
    b.adjust(1)
    return b.as_markup()


def back_main_kb(lang: str = "en") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t("btn_back_main", lang), callback_data="back:main")
    return b.as_markup()


def language_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for code, label in LANGUAGES.items():
        b.button(text=label, callback_data=f"lang:set:{code}")
    b.adjust(2)
    return b.as_markup()


def userbot_kb(lang: str, is_active: bool, miniapp_url: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if is_active:
        b.button(text=t("btn_disconnect_userbot", lang), callback_data="userbot:disconnect")
    else:
        b.button(
            text=t("btn_open_miniapp", lang),
            web_app=WebAppInfo(url=miniapp_url),
        )
    b.button(text=t("btn_back_main", lang), callback_data="back:main")
    b.adjust(1)
    return b.as_markup()


def admin_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📊 Статистика",      callback_data="admin:stats")
    b.button(text="👥 Пользователи",    callback_data="admin:users")
    b.button(text="📢 Рассылка",        callback_data="admin:broadcast")
    b.button(text="🔨 Бан / разбан",    callback_data="admin:ban")
    b.button(text="🎁 Подарить подписку", callback_data="admin:gift")
    b.adjust(2)
    return b.as_markup()


# helpers
def _days(lang): return {"ru":"дней","en":"days","pt":"dias","id":"hari"}.get(lang,"days")
def _year(lang): return {"ru":"год","en":"year","pt":"ano","id":"tahun"}.get(lang,"year")
