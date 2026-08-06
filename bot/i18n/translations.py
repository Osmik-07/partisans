"""
Переводы для BlackJaguar.
Языки: ru, en, pt, id
"""

LANGUAGES = {
    "ru": "Русский",
    "en": "English",
    "pt": "Português",
    "id": "Indonesia",
}

_T = {
    # ── Приветствие ──────────────────────────────────────────────────────
    "welcome": {
        "ru": (
            "🐾 <b>BlackJaguar</b> — знай всё, что скрывают\n\n"
            "<b>Единственный бот, который работает в фоне.</b>\n\n"
            "Бот перехватывает:\n"
            "• <b>Удалённые сообщения</b> — читай то, что удалили\n"
            "• <b>Правки сообщений</b> — сравни оригинал и изменённый текст\n"
            "• <b>Исчезающие фото/видео</b> — сохраняются навсегда\n\n"
            "Удалённые и изменённые сообщения работают <b>бесплатно</b> после подключения через "
            "<b>Настройки → Автоматизация чатов</b>.\n"
            "Одноразовые фото/видео доступны по подписке.\n\n"
            "Выбери действие:"
        ),
        "en": (
            "🐾 <b>BlackJaguar</b> — know everything they hide\n\n"
            "<b>The only bot that works in the background.</b>\n\n"
            "The bot intercepts:\n"
            "• <b>Deleted messages</b> — read what was deleted\n"
            "• <b>Edited messages</b> — compare original and edited text\n"
            "• <b>Disappearing photos/videos</b> — saved forever\n\n"
            "Deleted and edited messages work <b>for free</b> after connecting via "
            "<b>Settings → Chat Automation</b>.\n"
            "One-time photos/videos are available with a subscription.\n\n"
            "Choose an action:"
        ),
        "pt": (
            "🐾 <b>BlackJaguar</b> — saiba tudo que escondem\n\n"
            "<b>O único bot que funciona em segundo plano.</b>\n\n"
            "O bot intercepta:\n"
            "• <b>Mensagens apagadas</b> — leia o que foi apagado\n"
            "• <b>Mensagens editadas</b> — compare o original e o editado\n"
            "• <b>Fotos/vídeos temporários</b> — salvos para sempre\n\n"
            "Mensagens apagadas e editadas funcionam <b>grátis</b> após conectar via "
            "<b>Configurações → Automação de chats</b>.\n"
            "Fotos/vídeos temporários estão disponíveis com assinatura.\n\n"
            "Escolha uma ação:"
        ),
        "id": (
            "🐾 <b>BlackJaguar</b> — ketahui semua yang disembunyikan\n\n"
            "<b>Satu-satunya bot yang bekerja di latar belakang.</b>\n\n"
            "Bot ini menangkap:\n"
            "• <b>Pesan yang dihapus</b> — baca apa yang dihapus\n"
            "• <b>Pesan yang diedit</b> — bandingkan asli dan yang diedit\n"
            "• <b>Foto/video sementara</b> — tersimpan selamanya\n\n"
            "Pesan yang dihapus dan diedit berfungsi <b>gratis</b> setelah menghubungkan melalui "
            "<b>Pengaturan → Otomatisasi Chat</b>.\n"
            "Foto/video sekali-pakai tersedia dengan langganan.\n\n"
            "Pilih tindakan:"
        ),
    },

    # ── Выбор языка ──────────────────────────────────────────────────────
    "choose_language": {
        "ru": "Выбери язык:",
        "en": "Choose language:",
        "pt": "Escolha o idioma:",
        "id": "Pilih bahasa:",
    },
    "language_set": {
        "ru": "Язык установлен: Русский",
        "en": "Language set: English",
        "pt": "Idioma definido: Português",
        "id": "Bahasa dipilih: Indonesia",
    },

    # ── Меню ─────────────────────────────────────────────────────────────
    "btn_buy": {
        "ru": "Купить подписку",
        "en": "Buy subscription",
        "pt": "Comprar assinatura",
        "id": "Beli langganan",
    },
    "btn_status": {
        "ru": "Мой статус",
        "en": "My status",
        "pt": "Meu status",
        "id": "Status saya",
    },
    "btn_referral": {
        "ru": "Реферальная программа",
        "en": "Referral program",
        "pt": "Programa de indicação",
        "id": "Program referral",
    },
    "btn_connect": {
        "ru": "Как подключить",
        "en": "How to connect",
        "pt": "Como conectar",
        "id": "Cara menghubungkan",
    },
    "btn_language": {
        "ru": "Язык",
        "en": "Language",
        "pt": "Idioma",
        "id": "Bahasa",
    },
    "btn_userbot": {
        "ru": "Подключить перехват фото",
        "en": "Connect photo intercept",
        "pt": "Conectar interceptação de fotos",
        "id": "Hubungkan intersepsi foto",
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
    "btn_share_referral": {
        "ru": "Поделиться ссылкой",
        "en": "Share link",
        "pt": "Compartilhar link",
        "id": "Bagikan tautan",
    },

    # ── Подключение ───────────────────────────────────────────────────────
    "how_to_connect": {
        "ru": (
            "<b>Как подключить бота:</b>\n\n"
            "1. Открой <b>Настройки</b> в Telegram\n"
            "2. Перейди в <b>Автоматизация чатов</b>\n"
            "3. Выбери раздел <b>Чат-боты</b>\n"
            "4. Найди <b>@{bot_username}</b> и подключи его\n"
            "5. Разреши доступ ко <b>всем нужным чатам</b>\n\n"
            "Если у тебя старая версия Telegram, этот пункт может называться "
            "<b>Telegram для бизнеса → Чат-боты</b>.\n\n"
            "После подключения бот начнёт отслеживать сообщения в реальном времени."
        ),
        "en": (
            "<b>How to connect the bot:</b>\n\n"
            "1. Open <b>Settings</b> in Telegram\n"
            "2. Go to <b>Chat Automation</b>\n"
            "3. Open <b>Chat Bots</b>\n"
            "4. Find <b>@{bot_username}</b> and connect it\n"
            "5. Allow access to <b>all needed chats</b>\n\n"
            "On older Telegram versions, this section may be called "
            "<b>Telegram for Business → Chat Bots</b>.\n\n"
            "After connecting, the bot will start tracking messages in real time."
        ),
        "pt": (
            "<b>Como conectar o bot:</b>\n\n"
            "1. Abra as <b>Configurações</b> no Telegram\n"
            "2. Vá em <b>Automação de chats</b>\n"
            "3. Abra <b>Chatbots</b>\n"
            "4. Encontre <b>@{bot_username}</b> e conecte\n"
            "5. Permita acesso a <b>todos os chats necessários</b>\n\n"
            "Em versões antigas do Telegram, esta seção pode se chamar "
            "<b>Telegram para Empresas → Chatbots</b>.\n\n"
            "Após conectar, o bot começará a rastrear mensagens em tempo real."
        ),
        "id": (
            "<b>Cara menghubungkan bot:</b>\n\n"
            "1. Buka <b>Pengaturan</b> di Telegram\n"
            "2. Masuk ke <b>Otomatisasi Chat</b>\n"
            "3. Buka <b>Bot Chat</b>\n"
            "4. Temukan <b>@{bot_username}</b> dan hubungkan\n"
            "5. Izinkan akses ke <b>semua chat yang diperlukan</b>\n\n"
            "Pada versi Telegram lama, bagian ini mungkin bernama "
            "<b>Telegram untuk Bisnis → Bot Chat</b>.\n\n"
            "Setelah terhubung, bot akan mulai melacak pesan secara real time."
        ),
    },
    "referral_program": {
        "ru": (
            "<b>Реферальная программа</b>\n\n"
            "Здесь работают <b>2 разные реферальные программы</b>:\n\n"
            "<b>1. Бонус в Telegram Stars</b>\n"
            "Официальная программа Telegram. Ссылка для неё берётся в профиле бота.\n"
            "Смотри скриншот выше: он показывает, где именно открыть эту ссылку.\n"
            "Награда: <b>до {stars_percent}% в Stars</b> от оплаты приглашённого пользователя.\n\n"
            "<b>2. Бонусные дни в BlackJaguar</b>\n"
            "Используй свою личную ссылку ниже.\n"
            "За каждого нового пользователя, который запустит бота по ней, ты получаешь "
            "<b>{bonus_days}</b> бесплатный день.\n"
            "Если подписка уже активна, день просто прибавляется к оставшемуся сроку.\n\n"
            "Всего приглашено: <b>{invites_count}</b>\n"
            "Всего начислено бонусных дней: <b>{total_bonus_days}</b>\n\n"
            "<b>Твоя ссылка на бонусные дни:</b>\n"
            "<code>{referral_url}</code>"
        ),
        "en": (
            "<b>Referral program</b>\n\n"
            "There are <b>2 different referral programs</b> here:\n\n"
            "<b>1. Telegram Stars bonus</b>\n"
            "This is the official Telegram program. Its link is taken from the bot profile.\n"
            "See the screenshot above to find where to open it.\n"
            "Reward: <b>up to {stars_percent}% in Stars</b> from an invited user's payment.\n\n"
            "<b>2. Bonus days in BlackJaguar</b>\n"
            "Use your personal link below.\n"
            "For every new user who starts the bot from it, you get <b>{bonus_days}</b> free day.\n"
            "If your subscription is already active, the day is added to the remaining time.\n\n"
            "Total invited: <b>{invites_count}</b>\n"
            "Total bonus days earned: <b>{total_bonus_days}</b>\n\n"
            "<b>Your bonus-days link:</b>\n"
            "<code>{referral_url}</code>"
        ),
        "pt": (
            "<b>Programa de indicação</b>\n\n"
            "Aqui existem <b>2 programas de indicação diferentes</b>:\n\n"
            "<b>1. Bônus em Telegram Stars</b>\n"
            "Este é o programa oficial do Telegram. O link dele é obtido no perfil do bot.\n"
            "Veja a captura de tela acima para encontrar onde abri-lo.\n"
            "Recompensa: <b>até {stars_percent}% em Stars</b> do pagamento do usuário convidado.\n\n"
            "<b>2. Dias bônus no BlackJaguar</b>\n"
            "Use seu link pessoal abaixo.\n"
            "Para cada novo usuário que iniciar o bot por ele, você recebe <b>{bonus_days}</b> dia grátis.\n"
            "Se sua assinatura já estiver ativa, o dia é somado ao tempo restante.\n\n"
            "Total de convidados: <b>{invites_count}</b>\n"
            "Total de dias bônus: <b>{total_bonus_days}</b>\n\n"
            "<b>Seu link de dias bônus:</b>\n"
            "<code>{referral_url}</code>"
        ),
        "id": (
            "<b>Program referral</b>\n\n"
            "Di sini ada <b>2 program referral yang berbeda</b>:\n\n"
            "<b>1. Bonus Telegram Stars</b>\n"
            "Ini adalah program resmi Telegram. Tautannya diambil dari profil bot.\n"
            "Lihat screenshot di atas untuk mengetahui di mana membukanya.\n"
            "Hadiah: <b>hingga {stars_percent}% dalam Stars</b> dari pembayaran pengguna yang diundang.\n\n"
            "<b>2. Hari bonus di BlackJaguar</b>\n"
            "Gunakan tautan pribadi Anda di bawah ini.\n"
            "Untuk setiap pengguna baru yang menjalankan bot dari tautan itu, Anda mendapat <b>{bonus_days}</b> hari gratis.\n"
            "Jika langganan Anda sudah aktif, hari tersebut akan ditambahkan ke sisa waktu.\n\n"
            "Total undangan: <b>{invites_count}</b>\n"
            "Total hari bonus: <b>{total_bonus_days}</b>\n\n"
            "<b>Tautan hari bonus Anda:</b>\n"
            "<code>{referral_url}</code>"
        ),
    },
    "referral_share_text": {
        "ru": "Запусти BlackJaguar по моей ссылке",
        "en": "Start BlackJaguar with my referral link",
        "pt": "Inicie o BlackJaguar pelo meu link de indicação",
        "id": "Mulai BlackJaguar lewat tautan referral saya",
    },

    # ── Статус подписки ───────────────────────────────────────────────────
    "sub_active": {
        "ru": (
            "<b>Подписка активна</b>\n\n"
            "Тариф: <b>{plan}</b>\n"
            "Действует до: <b>{expires} UTC</b>\n\n"
            "Автоматизация чатов: {connected}"
        ),
        "en": (
            "<b>Subscription active</b>\n\n"
            "Plan: <b>{plan}</b>\n"
            "Valid until: <b>{expires} UTC</b>\n\n"
            "Chat Automation: {connected}"
        ),
        "pt": (
            "<b>Assinatura ativa</b>\n\n"
            "Plano: <b>{plan}</b>\n"
            "Válido até: <b>{expires} UTC</b>\n\n"
            "Automação de chats: {connected}"
        ),
        "id": (
            "<b>Langganan aktif</b>\n\n"
            "Paket: <b>{plan}</b>\n"
            "Berlaku hingga: <b>{expires} UTC</b>\n\n"
            "Otomatisasi Chat: {connected}"
        ),
    },
    "sub_inactive": {
        "ru": (
            "<b>Подписка не активна</b>\n\n"
            "Удалённые и изменённые сообщения доступны бесплатно после подключения через "
            "<b>Автоматизацию чатов</b>.\n\n"
            "Подписка нужна для перехвата одноразовых фото и видео."
        ),
        "en": (
            "<b>Subscription inactive</b>\n\n"
            "Deleted and edited messages are free after connecting via "
            "<b>Chat Automation</b>.\n\n"
            "A subscription is required for one-time photos and videos."
        ),
        "pt": (
            "<b>Assinatura inativa</b>\n\n"
            "Mensagens apagadas e editadas são grátis após conectar via "
            "<b>Automação de chats</b>.\n\n"
            "A assinatura é necessária para fotos e vídeos temporários."
        ),
        "id": (
            "<b>Langganan tidak aktif</b>\n\n"
            "Pesan yang dihapus dan diedit gratis setelah terhubung melalui "
            "<b>Otomatisasi Chat</b>.\n\n"
            "Langganan diperlukan untuk foto dan video sekali-pakai."
        ),
    },
    "sub_required_alert": {
        "ru": "Подписка нужна только для одноразовых медиа.",
        "en": "A subscription is required only for one-time media.",
        "pt": "A assinatura é necessária apenas para mídia temporária.",
        "id": "Langganan hanya diperlukan untuk media sekali-pakai.",
    },
    "trial_already_used": {
        "ru": "Пробный период уже использован.",
        "en": "Trial period has already been used.",
        "pt": "O período de teste já foi usado.",
        "id": "Masa percobaan sudah digunakan.",
    },
    "connected_yes": {
        "ru": "подключён",
        "en": "connected",
        "pt": "conectado",
        "id": "terhubung",
    },
    "connected_no": {
        "ru": "не подключён",
        "en": "not connected",
        "pt": "não conectado",
        "id": "tidak terhubung",
    },

    # ── Планы ─────────────────────────────────────────────────────────────
    "plans_title": {
        "ru": "<b>Выбери тариф:</b>",
        "en": "<b>Choose a plan:</b>",
        "pt": "<b>Escolha um plano:</b>",
        "id": "<b>Pilih paket:</b>",
    },
    "btn_trial": {
        "ru": "Пробный период — бесплатно",
        "en": "Trial period — free",
        "pt": "Período de teste — grátis",
        "id": "Periode percobaan — gratis",
    },
    "trial_activated": {
        "ru": (
            "<b>Пробный период активирован.</b>\n\n"
            "У тебя есть <b>{days} дня</b> для проверки бота.\n\n"
            "Не забудь подключить бота через Автоматизацию чатов."
        ),
        "en": (
            "<b>Trial period activated.</b>\n\n"
            "You have <b>{days} days</b> to test the bot.\n\n"
            "Don't forget to connect the bot via Chat Automation."
        ),
        "pt": (
            "<b>Período de teste ativado.</b>\n\n"
            "Você tem <b>{days} dias</b> para testar o bot.\n\n"
            "Não se esqueça de conectar o bot via Automação de chats."
        ),
        "id": (
            "<b>Periode percobaan diaktifkan.</b>\n\n"
            "Anda punya <b>{days} hari</b> untuk mencoba bot.\n\n"
            "Jangan lupa menghubungkan bot melalui Otomatisasi Chat."
        ),
    },

    # ── Userbot ────────────────────────────────────────────────────────────
    "userbot_title": {
        "ru": (
            "<b>Перехват исчезающих фото и видео</b>\n\n"
            "Для перехвата одноразовых медиа нужно авторизовать "
            "твой аккаунт Telegram.\n\n"
            "Нажми кнопку ниже — откроется безопасная форма авторизации."
        ),
        "en": (
            "<b>Intercept disappearing photos and videos</b>\n\n"
            "To intercept one-time media, you need to authorize "
            "your Telegram account.\n\n"
            "Click the button below — a secure authorization form will open."
        ),
        "pt": (
            "<b>Interceptar fotos e vídeos temporários</b>\n\n"
            "Para interceptar mídia de uso único, você precisa autorizar "
            "sua conta do Telegram.\n\n"
            "Clique no botão abaixo — um formulário de autorização seguro será aberto."
        ),
        "id": (
            "<b>Intersepsi foto dan video sementara</b>\n\n"
            "Untuk menangkap media sekali-pakai, Anda perlu mengotorisasi "
            "akun Telegram Anda.\n\n"
            "Klik tombol di bawah — formulir otorisasi yang aman akan terbuka."
        ),
    },
    "btn_open_miniapp": {
        "ru": "Авторизоваться",
        "en": "Authorize",
        "pt": "Autorizar",
        "id": "Otorisasi",
    },
    "userbot_active": {
        "ru": (
            "<b>Перехват активен</b>\n\n"
            "Одноразовые фото и видео будут приходить тебе как файлы."
        ),
        "en": (
            "<b>Interception active</b>\n\n"
            "One-time photos and videos will be sent to you as files."
        ),
        "pt": (
            "<b>Interceptação ativa</b>\n\n"
            "Fotos e vídeos temporários serão enviados a você como arquivos."
        ),
        "id": (
            "<b>Intersepsi aktif</b>\n\n"
            "Foto dan video sekali-pakai akan dikirim kepada Anda sebagai file."
        ),
    },
    "btn_disconnect_userbot": {
        "ru": "Отключить перехват",
        "en": "Disconnect interception",
        "pt": "Desconectar interceptação",
        "id": "Putuskan intersepsi",
    },

    # ── Бизнес-события ────────────────────────────────────────────────────
    "deleted_title": {
        "ru": "Удалённое сообщение",
        "en": "Deleted message",
        "pt": "Mensagem apagada",
        "id": "Pesan dihapus",
    },
    "edited_title": {
        "ru": "Изменённое сообщение",
        "en": "Edited message",
        "pt": "Mensagem editada",
        "id": "Pesan diedit",
    },
    "vanishing_title": {
        "ru": "Одноразовое медиа",
        "en": "One-time media",
        "pt": "Mídia temporária",
        "id": "Media sekali-pakai",
    },
    "sender_label": {
        "ru": "Отправитель",
        "en": "Sender",
        "pt": "Remetente",
        "id": "Pengirim",
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
    "media_photo": {
        "ru": "[Фото]",
        "en": "[Photo]",
        "pt": "[Foto]",
        "id": "[Foto]",
    },
    "media_video": {
        "ru": "[Видео]",
        "en": "[Video]",
        "pt": "[Vídeo]",
        "id": "[Video]",
    },
    "media_animation": {
        "ru": "[GIF]",
        "en": "[GIF]",
        "pt": "[GIF]",
        "id": "[GIF]",
    },
    "media_audio": {
        "ru": "[Аудио]",
        "en": "[Audio]",
        "pt": "[Áudio]",
        "id": "[Audio]",
    },
    "media_voice": {
        "ru": "[Голосовое]",
        "en": "[Voice message]",
        "pt": "[Mensagem de voz]",
        "id": "[Pesan suara]",
    },
    "media_video_note": {
        "ru": "[Видеосообщение]",
        "en": "[Video note]",
        "pt": "[Vídeo circular]",
        "id": "[Pesan video]",
    },
    "media_sticker": {
        "ru": "[Стикер]",
        "en": "[Sticker]",
        "pt": "[Sticker]",
        "id": "[Stiker]",
    },
    "media_document": {
        "ru": "[Документ]",
        "en": "[Document]",
        "pt": "[Documento]",
        "id": "[Dokumen]",
    },
    "media_unknown": {
        "ru": "[Медиа без текста]",
        "en": "[Media without text]",
        "pt": "[Mídia sem texto]",
        "id": "[Media tanpa teks]",
    },
    "command_start_desc": {
        "ru": "Главное меню",
        "en": "Open main menu",
        "pt": "Abrir menu principal",
        "id": "Buka menu utama",
    },
    "command_premium_desc": {
        "ru": "Подписка на одноразовые медиа",
        "en": "One-time media subscription",
        "pt": "Assinatura de mídia temporária",
        "id": "Langganan media sekali-pakai",
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
