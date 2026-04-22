"""
Переводы для Partisans.
Языки: ru, en, pt, id
"""

LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "id": "🇮🇩 Indonesia",
}

_T = {
    # ── Приветствие ──────────────────────────────────────────────────────
    "welcome": {
        "ru": (
            "🫆 <b>Partisans</b> — знай всё, что скрывают\n\n"
            "Бот перехватывает:\n"
            "• 🗑 <b>Удалённые сообщения</b> — читай то, что удалили\n"
            "• ✏️ <b>Правки сообщений</b> — сравни оригинал и изменённый текст\n"
            "• 📸 <b>Исчезающие фото/видео</b> — сохраняются навсегда\n\n"
            "⚠️ Для работы нужен <b>Telegram Premium</b> и подключение через "
            "<b>Настройки → Telegram для бизнеса → Чат-боты</b>.\n\n"
            "Выбери действие:"
        ),
        "en": (
            "🫆 <b>Partisans</b> — know everything they hide\n\n"
            "The bot intercepts:\n"
            "• 🗑 <b>Deleted messages</b> — read what was deleted\n"
            "• ✏️ <b>Edited messages</b> — compare original and edited text\n"
            "• 📸 <b>Disappearing photos/videos</b> — saved forever\n\n"
            "⚠️ Requires <b>Telegram Premium</b> and connection via "
            "<b>Settings → Telegram for Business → Chat Bots</b>.\n\n"
            "Choose an action:"
        ),
        "pt": (
            "🫆 <b>Partisans</b> — saiba tudo que escondem\n\n"
            "O bot intercepta:\n"
            "• 🗑 <b>Mensagens apagadas</b> — leia o que foi apagado\n"
            "• ✏️ <b>Mensagens editadas</b> — compare o original e o editado\n"
            "• 📸 <b>Fotos/vídeos temporários</b> — salvos para sempre\n\n"
            "⚠️ Requer <b>Telegram Premium</b> e conexão via "
            "<b>Configurações → Telegram para Empresas → Chatbots</b>.\n\n"
            "Escolha uma ação:"
        ),
        "id": (
            "🫆 <b>Partisans</b> — ketahui semua yang disembunyikan\n\n"
            "Bot ini menangkap:\n"
            "• 🗑 <b>Pesan yang dihapus</b> — baca apa yang dihapus\n"
            "• ✏️ <b>Pesan yang diedit</b> — bandingkan asli dan yang diedit\n"
            "• 📸 <b>Foto/video sementara</b> — tersimpan selamanya\n\n"
            "⚠️ Membutuhkan <b>Telegram Premium</b> dan koneksi melalui "
            "<b>Pengaturan → Telegram untuk Bisnis → Bot Chat</b>.\n\n"
            "Pilih tindakan:"
        ),
    },

    # ── Выбор языка ──────────────────────────────────────────────────────
    "choose_language": {
        "ru": "🌍 Выбери язык:",
        "en": "🌍 Choose language:",
        "pt": "🌍 Escolha o idioma:",
        "id": "🌍 Pilih bahasa:",
    },
    "language_set": {
        "ru": "✅ Язык установлен: Русский",
        "en": "✅ Language set: English",
        "pt": "✅ Idioma definido: Português",
        "id": "✅ Bahasa dipilih: Indonesia",
    },

    # ── Меню ─────────────────────────────────────────────────────────────
    "btn_buy": {
        "ru": "💎 Купить подписку",
        "en": "💎 Buy subscription",
        "pt": "💎 Comprar assinatura",
        "id": "💎 Beli langganan",
    },
    "btn_status": {
        "ru": "📊 Мой статус",
        "en": "📊 My status",
        "pt": "📊 Meu status",
        "id": "📊 Status saya",
    },
    "btn_connect": {
        "ru": "❓ Как подключить",
        "en": "❓ How to connect",
        "pt": "❓ Como conectar",
        "id": "❓ Cara menghubungkan",
    },
    "btn_language": {
        "ru": "🌍 Язык",
        "en": "🌍 Language",
        "pt": "🌍 Idioma",
        "id": "🌍 Bahasa",
    },
    "btn_userbot": {
        "ru": "📸 Подключить перехват фото",
        "en": "📸 Connect photo intercept",
        "pt": "📸 Conectar interceptação de fotos",
        "id": "📸 Hubungkan intersepsi foto",
    },
    "btn_back": {
        "ru": "« Назад",
        "en": "« Back",
        "pt": "« Voltar",
        "id": "« Kembali",
    },
    "btn_back_main": {
        "ru": "« Главное меню",
        "en": "« Main menu",
        "pt": "« Menu principal",
        "id": "« Menu utama",
    },

    # ── Подключение ───────────────────────────────────────────────────────
    "how_to_connect": {
        "ru": (
            "📌 <b>Как подключить бота:</b>\n\n"
            "1. Убедись, что у тебя активен <b>Telegram Premium</b>\n"
            "2. Открой <b>Настройки</b> в Telegram\n"
            "3. Перейди в <b>Telegram для бизнеса</b>\n"
            "4. Выбери <b>Чат-боты</b>\n"
            "5. Найди <b>@{bot_username}</b> и подключи\n"
            "6. Разреши доступ ко <b>всем чатам</b>\n\n"
            "После подключения бот начнёт отслеживать сообщения в реальном времени."
        ),
        "en": (
            "📌 <b>How to connect the bot:</b>\n\n"
            "1. Make sure you have active <b>Telegram Premium</b>\n"
            "2. Open <b>Settings</b> in Telegram\n"
            "3. Go to <b>Telegram for Business</b>\n"
            "4. Select <b>Chat Bots</b>\n"
            "5. Find <b>@{bot_username}</b> and connect\n"
            "6. Allow access to <b>all chats</b>\n\n"
            "After connecting, the bot will start tracking messages in real time."
        ),
        "pt": (
            "📌 <b>Como conectar o bot:</b>\n\n"
            "1. Certifique-se de ter o <b>Telegram Premium</b> ativo\n"
            "2. Abra as <b>Configurações</b> no Telegram\n"
            "3. Vá em <b>Telegram para Empresas</b>\n"
            "4. Selecione <b>Chatbots</b>\n"
            "5. Encontre <b>@{bot_username}</b> e conecte\n"
            "6. Permita acesso a <b>todos os chats</b>\n\n"
            "Após conectar, o bot começará a rastrear mensagens em tempo real."
        ),
        "id": (
            "📌 <b>Cara menghubungkan bot:</b>\n\n"
            "1. Pastikan Anda memiliki <b>Telegram Premium</b> aktif\n"
            "2. Buka <b>Pengaturan</b> di Telegram\n"
            "3. Pergi ke <b>Telegram untuk Bisnis</b>\n"
            "4. Pilih <b>Bot Chat</b>\n"
            "5. Temukan <b>@{bot_username}</b> dan hubungkan\n"
            "6. Izinkan akses ke <b>semua obrolan</b>\n\n"
            "Setelah terhubung, bot akan mulai melacak pesan secara real time."
        ),
    },

    # ── Статус подписки ───────────────────────────────────────────────────
    "sub_active": {
        "ru": (
            "✅ <b>Подписка активна</b>\n\n"
            "Тариф: <b>{plan}</b>\n"
            "Действует до: <b>{expires} UTC</b>\n\n"
            "Бизнес-бот: {connected}"
        ),
        "en": (
            "✅ <b>Subscription active</b>\n\n"
            "Plan: <b>{plan}</b>\n"
            "Valid until: <b>{expires} UTC</b>\n\n"
            "Business bot: {connected}"
        ),
        "pt": (
            "✅ <b>Assinatura ativa</b>\n\n"
            "Plano: <b>{plan}</b>\n"
            "Válido até: <b>{expires} UTC</b>\n\n"
            "Bot de negócios: {connected}"
        ),
        "id": (
            "✅ <b>Langganan aktif</b>\n\n"
            "Paket: <b>{plan}</b>\n"
            "Berlaku hingga: <b>{expires} UTC</b>\n\n"
            "Bot bisnis: {connected}"
        ),
    },
    "sub_inactive": {
        "ru": "❌ <b>Подписка не активна</b>\n\nКупи подписку, чтобы начать отслеживание.",
        "en": "❌ <b>Subscription inactive</b>\n\nBuy a subscription to start tracking.",
        "pt": "❌ <b>Assinatura inativa</b>\n\nCompre uma assinatura para começar a rastrear.",
        "id": "❌ <b>Langganan tidak aktif</b>\n\nBeli langganan untuk mulai melacak.",
    },
    "sub_required_alert": {
        "ru": "Нужна активная подписка.",
        "en": "An active subscription is required.",
        "pt": "É necessária uma assinatura ativa.",
        "id": "Langganan aktif diperlukan.",
    },
    "trial_already_used": {
        "ru": "Пробный период уже использован.",
        "en": "Trial period has already been used.",
        "pt": "O período de teste já foi usado.",
        "id": "Masa percobaan sudah digunakan.",
    },
    "connected_yes": {
        "ru": "🟢 подключён",
        "en": "🟢 connected",
        "pt": "🟢 conectado",
        "id": "🟢 terhubung",
    },
    "connected_no": {
        "ru": "🔴 не подключён",
        "en": "🔴 not connected",
        "pt": "🔴 não conectado",
        "id": "🔴 tidak terhubung",
    },

    # ── Планы ─────────────────────────────────────────────────────────────
    "plans_title": {
        "ru": "💎 <b>Выбери тариф:</b>",
        "en": "💎 <b>Choose a plan:</b>",
        "pt": "💎 <b>Escolha um plano:</b>",
        "id": "💎 <b>Pilih paket:</b>",
    },
    "btn_trial": {
        "ru": "🎁 Пробный период — БЕСПЛАТНО",
        "en": "🎁 Trial period — FREE",
        "pt": "🎁 Período de teste — GRÁTIS",
        "id": "🎁 Periode percobaan — GRATIS",
    },
    "trial_activated": {
        "ru": (
            "🎁 <b>Пробный период активирован!</b>\n\n"
            "У тебя есть <b>{days} дня</b> для проверки бота.\n\n"
            "Не забудь подключить бота через Telegram для бизнеса."
        ),
        "en": (
            "🎁 <b>Trial period activated!</b>\n\n"
            "You have <b>{days} days</b> to test the bot.\n\n"
            "Don't forget to connect the bot via Telegram for Business."
        ),
        "pt": (
            "🎁 <b>Período de teste ativado!</b>\n\n"
            "Você tem <b>{days} dias</b> para testar o bot.\n\n"
            "Não se esqueça de conectar o bot via Telegram para Empresas."
        ),
        "id": (
            "🎁 <b>Periode percobaan diaktifkan!</b>\n\n"
            "Anda punya <b>{days} hari</b> untuk mencoba bot.\n\n"
            "Jangan lupa menghubungkan bot melalui Telegram untuk Bisnis."
        ),
    },

    # ── Userbot ────────────────────────────────────────────────────────────
    "userbot_title": {
        "ru": (
            "📸 <b>Перехват исчезающих фото и видео</b>\n\n"
            "Для перехвата одноразовых медиа нужно авторизовать "
            "твой аккаунт Telegram.\n\n"
            "Нажми кнопку ниже — откроется безопасная форма авторизации."
        ),
        "en": (
            "📸 <b>Intercept disappearing photos and videos</b>\n\n"
            "To intercept one-time media, you need to authorize "
            "your Telegram account.\n\n"
            "Click the button below — a secure authorization form will open."
        ),
        "pt": (
            "📸 <b>Interceptar fotos e vídeos temporários</b>\n\n"
            "Para interceptar mídia de uso único, você precisa autorizar "
            "sua conta do Telegram.\n\n"
            "Clique no botão abaixo — um formulário de autorização seguro será aberto."
        ),
        "id": (
            "📸 <b>Intersepsi foto dan video sementara</b>\n\n"
            "Untuk menangkap media sekali-pakai, Anda perlu mengotorisasi "
            "akun Telegram Anda.\n\n"
            "Klik tombol di bawah — formulir otorisasi yang aman akan terbuka."
        ),
    },
    "btn_open_miniapp": {
        "ru": "📱 Авторизоваться",
        "en": "📱 Authorize",
        "pt": "📱 Autorizar",
        "id": "📱 Otorisasi",
    },
    "userbot_active": {
        "ru": (
            "✅ <b>Перехват активен</b>\n\n"
            "Одноразовые фото и видео будут приходить тебе как файлы."
        ),
        "en": (
            "✅ <b>Interception active</b>\n\n"
            "One-time photos and videos will be sent to you as files."
        ),
        "pt": (
            "✅ <b>Interceptação ativa</b>\n\n"
            "Fotos e vídeos temporários serão enviados a você como arquivos."
        ),
        "id": (
            "✅ <b>Intersepsi aktif</b>\n\n"
            "Foto dan video sekali-pakai akan dikirim kepada Anda sebagai file."
        ),
    },
    "btn_disconnect_userbot": {
        "ru": "🔴 Отключить перехват",
        "en": "🔴 Disconnect interception",
        "pt": "🔴 Desconectar interceptação",
        "id": "🔴 Putuskan intersepsi",
    },

    # ── Бизнес-события ────────────────────────────────────────────────────
    "deleted_header": {
        "ru": "🗑 <b>{name} удалил(а) сообщение</b>",
        "en": "🗑 <b>{name} deleted a message</b>",
        "pt": "🗑 <b>{name} apagou uma mensagem</b>",
        "id": "🗑 <b>{name} menghapus pesan</b>",
    },
    "edited_header": {
        "ru": "✏️ <b>{name} изменил(а) сообщение</b>",
        "en": "✏️ <b>{name} edited a message</b>",
        "pt": "✏️ <b>{name} editou uma mensagem</b>",
        "id": "✏️ <b>{name} mengedit pesan</b>",
    },
    "was": {
        "ru": "Было:",
        "en": "Was:",
        "pt": "Era:",
        "id": "Sebelumnya:",
    },
    "became": {
        "ru": "Стало:",
        "en": "Became:",
        "pt": "Ficou:",
        "id": "Menjadi:",
    },
    "not_saved": {
        "ru": "(не сохранено)",
        "en": "(not saved)",
        "pt": "(não salvo)",
        "id": "(tidak tersimpan)",
    },
    "vanishing_header": {
        "ru": "📸 <b>Одноразовое медиа</b> от <b>{name}</b>\n\n@partisansfromNJbot",
        "en": "📸 <b>One-time media</b> from <b>{name}</b>\n\n@partisansfromNJbot",
        "pt": "📸 <b>Mídia temporária</b> de <b>{name}</b>\n\n@partisansfromNJbot",
        "id": "📸 <b>Media sekali-pakai</b> dari <b>{name}</b>\n\n@partisansfromNJbot",
    },
}


def get_lang(language_code: str | None) -> str:
    """Возвращает код языка если поддерживается, иначе 'en'."""
    if language_code and language_code[:2] in LANGUAGES:
        return language_code[:2]
    return "en"


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Получить перевод по ключу."""
    translations = _T.get(key, {})
    text = translations.get(lang) or translations.get("en", f"[{key}]")
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text
