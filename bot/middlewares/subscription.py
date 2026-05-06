from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.i18n import t
from bot.keyboards.main import plans_kb
from bot.services.subscription import get_active_subscription, get_user

# Команды/колбэки, доступные без подписки
FREE_COMMANDS = {"/start", "/help", "/userbot", "/premium"}
FREE_CALLBACKS = {"sub:", "buy:", "pay:", "back:", "help:", "userbot:disconnect"}



class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        # Проверяем только Message и CallbackQuery
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        user_id = event.from_user.id if event.from_user else None
        if not user_id:
            return await handler(event, data)

        if isinstance(event, Message) and getattr(event, "business_connection_id", None):
            return await handler(event, data)

        # Пропускаем свободные команды
        if isinstance(event, Message) and event.text:
            cmd = event.text.split()[0].lower()
            if cmd in FREE_COMMANDS:
                return await handler(event, data)

        if isinstance(event, CallbackQuery) and event.data:
            for prefix in FREE_CALLBACKS:
                if event.data.startswith(prefix):
                    return await handler(event, data)

        # Проверяем подписку
        session = data.get("session")
        user = await get_user(session, user_id) if session else None
        from bot.config import settings
        if user_id in settings.admin_ids:
            return await handler(event, data)

        if not user:
            return await handler(event, data)

        if user.is_banned:
            if isinstance(event, Message):
                await event.answer("Ваш аккаунт заблокирован.")
            elif isinstance(event, CallbackQuery):
                await event.answer("Ваш аккаунт заблокирован.", show_alert=True)
            return

        active_sub = await get_active_subscription(session, user_id) if session else None
        if active_sub:
            return await handler(event, data)

        lang = user.lang if user.lang else "en"
        if isinstance(event, Message):
            await event.answer(
                t("sub_inactive", lang),
                reply_markup=plans_kb(lang, trial_available=not user.trial_used),
                parse_mode="HTML",
            )
        elif isinstance(event, CallbackQuery):
            await event.answer(
                t("sub_required_alert", lang),
                show_alert=True,
            )
        return
