from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from urllib.parse import quote
from bot.config import settings
from bot.i18n import t, LANGUAGES


def main_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t("btn_buy", lang),     callback_data="sub:plans")
    b.button(text=t("btn_status", lang),  callback_data="sub:status")
    b.button(text=t("btn_referral", lang), callback_data="ref:menu")
    b.button(text=t("btn_connect", lang), callback_data="help:connect")
    b.button(text=t("btn_userbot", lang), callback_data="userbot:menu")
    b.button(text=t("btn_protection", lang), callback_data="protect:menu")
    b.button(text=t("btn_language", lang),callback_data="lang:menu")
    b.adjust(1)
    return b.as_markup()


def plans_kb(lang: str = "en", trial_available: bool = False) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if trial_available:
        b.button(text=t("btn_trial", lang), callback_data="buy:trial")
    b.button(text=f"7 {_days(lang)} — ${settings.price_week_usd:.2f}",  callback_data="buy:week")
    b.button(text=f"30 {_days(lang)} — ${settings.price_month_usd:.2f}", callback_data="buy:month")
    b.button(text=f"1 {_year(lang)} — ${settings.price_year_usd:.2f}",   callback_data="buy:year")
    b.button(text=t("btn_back", lang), callback_data="back:main")
    b.adjust(1)
    return b.as_markup()


def payment_method_kb(plan: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="CryptoBot", callback_data=f"pay:crypto:{plan}")
    builder.button(text="Telegram Stars", callback_data=f"pay:stars:{plan}")
    builder.button(text="« Назад", callback_data="sub:plans")
    builder.adjust(1)
    return builder.as_markup()


def pay_crypto_kb(pay_url: str, payment_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить", url=pay_url)
    builder.button(text="Я оплатил", callback_data=f"pay:check:{payment_id}")
    builder.button(text="« Отмена", callback_data="sub:plans")
    builder.adjust(1)
    return builder.as_markup()


def back_main_kb(lang: str = "en") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t("btn_back_main", lang), callback_data="back:main")
    return b.as_markup()


def referral_kb(lang: str, referral_url: str, share_text: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    share_url = f"https://t.me/share/url?url={quote(referral_url, safe='')}&text={quote(share_text, safe='')}"
    b.button(
        text=t("btn_share_referral", lang),
        url=share_url,
    )
    b.button(text=t("btn_back_main", lang), callback_data="back:main")
    b.adjust(1)
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


def protection_kb(lang: str, already_protected: bool) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if not already_protected:
        b.button(
            text=f"{t('btn_buy_protection', lang)} — ${settings.price_protection_usd:.0f}",
            callback_data="protect:pay",
        )
    b.button(text=t("btn_back_main", lang), callback_data="back:main")
    b.adjust(1)
    return b.as_markup()


def protection_method_kb(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="CryptoBot", callback_data="protect:crypto")
    b.button(text="Telegram Stars", callback_data="protect:stars")
    b.button(text=t("btn_back", lang), callback_data="protect:menu")
    b.adjust(1)
    return b.as_markup()


def admin_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Статистика", callback_data="admin:stats")
    b.button(text="Пользователи", callback_data="admin:users")
    b.button(text="Рассылка", callback_data="admin:broadcast")
    b.button(text="Бан / разбан", callback_data="admin:ban")
    b.button(text="Подарить подписку", callback_data="admin:gift")
    b.button(text="Подарить защиту", callback_data="admin:gift_protection")
    b.adjust(2)
    return b.as_markup()


# helpers
def _days(lang): return {"ru":"дней","en":"days","pt":"dias","id":"hari"}.get(lang,"days")
def _year(lang): return {"ru":"год","en":"year","pt":"ano","id":"tahun"}.get(lang,"year")
