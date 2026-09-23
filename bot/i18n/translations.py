"""
Переводы для Partisans.
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
            "🐾 <b>Partisans mekbuda</b>\n\n"
            "<b>Ни одно сообщение больше не исчезнет бесследно.</b>\n\n"
            "Собеседник удалил переписку, поправил слова задним числом или прислал "
            "самоуничтожающееся фото? Ты видишь пустоту — Partisans видит всё.\n\n"
            "<b>🗑 Удалённые сообщения</b>\n"
            "Прилетают тебе, даже если их стёрли через секунду.\n\n"
            "<b>✏️ Изменённые сообщения</b>\n"
            "Показываем оригинал — то, что написали на самом деле.\n\n"
            "<b>👻 Исчезающие фото и видео</b>\n"
            "Остаются у тебя навсегда, а не на пару секунд.\n\n"
            "🎁 <b>Удалённые и правки — бесплатно.</b> Подключается за минуту:\n"
            "<b>Настройки → Автоматизация чатов → Чат-боты → добавь этого бота → "
            "разреши доступ к чатам.</b>\n\n"
            "🔓 <b>Исчезающие фото и видео — по подписке.</b> Настроил один раз — "
            "работает в фоне.\n\n"
            "Выбери, с чего начать 👇"
        ),
        "en": (
            "🐾 <b>Partisans mekbuda</b>\n\n"
            "<b>No message disappears without a trace anymore.</b>\n\n"
            "Someone deleted the chat, edited their words after the fact, or sent a "
            "self-destructing photo? You see a blank — Partisans sees everything.\n\n"
            "<b>🗑 Deleted messages</b>\n"
            "Land in your chat even if they were wiped a second later.\n\n"
            "<b>✏️ Edited messages</b>\n"
            "We show the original — what was really written.\n\n"
            "<b>👻 Disappearing photos and videos</b>\n"
            "Stay with you forever, not for a couple of seconds.\n\n"
            "🎁 <b>Deleted and edits — free.</b> Takes a minute to connect:\n"
            "<b>Settings → Chat Automation → Chat Bots → add this bot → "
            "allow access to your chats.</b>\n\n"
            "🔓 <b>Disappearing photos and videos — with a subscription.</b> Set it up "
            "once — it works in the background.\n\n"
            "Pick where to start 👇"
        ),
        "pt": (
            "🐾 <b>Partisans mekbuda</b>\n\n"
            "<b>Nenhuma mensagem desaparece sem deixar rasto.</b>\n\n"
            "Apagaram a conversa, editaram as palavras depois ou enviaram uma foto que "
            "se autodestrói? Você vê o vazio — o Partisans vê tudo.\n\n"
            "<b>🗑 Mensagens apagadas</b>\n"
            "Chegam até você mesmo que apaguem um segundo depois.\n\n"
            "<b>✏️ Mensagens editadas</b>\n"
            "Mostramos o original — o que foi realmente escrito.\n\n"
            "<b>👻 Fotos e vídeos temporários</b>\n"
            "Ficam com você para sempre, não por alguns segundos.\n\n"
            "🎁 <b>Apagadas e edições — grátis.</b> Conecta em um minuto:\n"
            "<b>Configurações → Automação de chats → Chatbots → adicione este bot → "
            "permita acesso aos chats.</b>\n\n"
            "🔓 <b>Fotos e vídeos temporários — com assinatura.</b> Configure uma vez — "
            "funciona em segundo plano.\n\n"
            "Escolha por onde começar 👇"
        ),
        "id": (
            "🐾 <b>Partisans mekbuda</b>\n\n"
            "<b>Tidak ada pesan yang hilang tanpa jejak lagi.</b>\n\n"
            "Lawan bicara menghapus obrolan, mengubah kata belakangan, atau mengirim foto "
            "yang menghancurkan diri? Anda melihat kosong — Partisans melihat semuanya.\n\n"
            "<b>🗑 Pesan yang dihapus</b>\n"
            "Tetap sampai ke Anda meski dihapus sedetik kemudian.\n\n"
            "<b>✏️ Pesan yang diedit</b>\n"
            "Kami tampilkan aslinya — yang benar-benar ditulis.\n\n"
            "<b>👻 Foto dan video sementara</b>\n"
            "Tersimpan selamanya, bukan cuma beberapa detik.\n\n"
            "🎁 <b>Dihapus dan diedit — gratis.</b> Terhubung dalam satu menit:\n"
            "<b>Pengaturan → Otomatisasi Chat → Bot Chat → tambahkan bot ini → "
            "izinkan akses ke chat.</b>\n\n"
            "🔓 <b>Foto dan video sementara — dengan langganan.</b> Atur sekali — "
            "bekerja di latar belakang.\n\n"
            "Pilih dari mana memulai 👇"
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
        "ru": "🔓 Открыть исчезающие фото",
        "en": "🔓 Unlock disappearing photos",
        "pt": "🔓 Abrir fotos que somem",
        "id": "🔓 Buka foto yang menghilang",
    },
    "btn_status": {
        "ru": "👤 Мой статус",
        "en": "👤 My status",
        "pt": "👤 Meu status",
        "id": "👤 Status saya",
    },
    "btn_referral": {
        "ru": "🎁 Пригласить друзей",
        "en": "🎁 Invite friends",
        "pt": "🎁 Convidar amigos",
        "id": "🎁 Undang teman",
    },
    "btn_connect": {
        "ru": "📲 Как подключить",
        "en": "📲 How to connect",
        "pt": "📲 Como conectar",
        "id": "📲 Cara menghubungkan",
    },
    "btn_language": {
        "ru": "🌐 Язык",
        "en": "🌐 Language",
        "pt": "🌐 Idioma",
        "id": "🌐 Bahasa",
    },
    "btn_userbot": {
        "ru": "👻 Ловить исчезающие медиа",
        "en": "👻 Catch disappearing media",
        "pt": "👻 Capturar mídia que some",
        "id": "👻 Tangkap media menghilang",
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
            "<b>Подключение за 1 минуту</b>\n\n"
            "Нужен <b>Telegram Premium</b> — режим для бизнеса включается только на нём.\n\n"
            "<b>1.</b> Открой <b>Настройки</b> в Telegram\n"
            "<b>2.</b> Зайди в <b>Автоматизация чатов</b>\n"
            "   <i>(в старых версиях — «Telegram для бизнеса»)</i>\n"
            "<b>3.</b> Выбери <b>Чат-боты</b>\n"
            "<b>4.</b> Впиши <b>@{bot_username}</b> и добавь\n"
            "<b>5.</b> Разреши доступ к чатам, которые хочешь защитить\n\n"
            "Готово. Дальше бот работает сам: как только в чате удалят или изменят "
            "сообщение — оно тут же прилетит тебе.\n\n"
            "🎁 Удалённые и изменённые сообщения — <b>бесплатно, без подписки.</b>"
        ),
        "en": (
            "<b>Connect in 1 minute</b>\n\n"
            "You need <b>Telegram Premium</b> — the business mode only turns on with it.\n\n"
            "<b>1.</b> Open <b>Settings</b> in Telegram\n"
            "<b>2.</b> Go to <b>Chat Automation</b>\n"
            "   <i>(on older versions — “Telegram Business”)</i>\n"
            "<b>3.</b> Open <b>Chat Bots</b>\n"
            "<b>4.</b> Enter <b>@{bot_username}</b> and add it\n"
            "<b>5.</b> Allow access to the chats you want to protect\n\n"
            "Done. From here the bot runs on its own: the moment a message is deleted or "
            "edited in a chat, it lands in yours.\n\n"
            "🎁 Deleted and edited messages — <b>free, no subscription.</b>"
        ),
        "pt": (
            "<b>Conecte em 1 minuto</b>\n\n"
            "É preciso <b>Telegram Premium</b> — o modo empresarial só ativa com ele.\n\n"
            "<b>1.</b> Abra as <b>Configurações</b> no Telegram\n"
            "<b>2.</b> Vá em <b>Automação de chats</b>\n"
            "   <i>(em versões antigas — “Telegram para Empresas”)</i>\n"
            "<b>3.</b> Abra <b>Chatbots</b>\n"
            "<b>4.</b> Digite <b>@{bot_username}</b> e adicione\n"
            "<b>5.</b> Permita acesso aos chats que quer proteger\n\n"
            "Pronto. A partir daí o bot trabalha sozinho: assim que apagarem ou editarem "
            "uma mensagem num chat, ela chega até você.\n\n"
            "🎁 Mensagens apagadas e editadas — <b>grátis, sem assinatura.</b>"
        ),
        "id": (
            "<b>Hubungkan dalam 1 menit</b>\n\n"
            "Perlu <b>Telegram Premium</b> — mode bisnis hanya aktif dengannya.\n\n"
            "<b>1.</b> Buka <b>Pengaturan</b> di Telegram\n"
            "<b>2.</b> Masuk ke <b>Otomatisasi Chat</b>\n"
            "   <i>(pada versi lama — “Telegram Bisnis”)</i>\n"
            "<b>3.</b> Buka <b>Bot Chat</b>\n"
            "<b>4.</b> Ketik <b>@{bot_username}</b> lalu tambahkan\n"
            "<b>5.</b> Izinkan akses ke chat yang ingin Anda lindungi\n\n"
            "Selesai. Selanjutnya bot bekerja sendiri: begitu sebuah pesan dihapus atau "
            "diedit di chat, pesan itu langsung sampai ke Anda.\n\n"
            "🎁 Pesan yang dihapus dan diedit — <b>gratis, tanpa langganan.</b>"
        ),
    },
    "referral_program": {
        "ru": (
            "<b>Приглашай друзей — зарабатывай дважды</b>\n\n"
            "У тебя работают <b>две программы одновременно.</b>\n\n"
            "<b>💰 1. Stars за каждую оплату</b>\n"
            "Официальная программа Telegram. Возвращает тебе <b>до {stars_percent}% в Stars</b> "
            "с каждой оплаты приглашённого — снова и снова, а не один раз.\n"
            "Ссылка для неё — в профиле бота: открой карточку бота и нажми "
            "<b>«Пригласить друзей»</b> (или <b>«Мои Stars»</b>).\n\n"
            "<b>🎁 2. Бесплатные дни подписки</b>\n"
            "За каждого, кто впервые запустит бота по твоей ссылке ниже, — "
            "<b>+{bonus_days} день</b> к подписке. Есть активная — просто прибавим к сроку.\n\n"
            "Уже приглашено: <b>{invites_count}</b>\n"
            "Начислено дней: <b>{total_bonus_days}</b>\n\n"
            "<b>Твоя ссылка:</b>\n"
            "<code>{referral_url}</code>"
        ),
        "en": (
            "<b>Invite friends — earn twice</b>\n\n"
            "You have <b>two programs running at once.</b>\n\n"
            "<b>💰 1. Stars on every payment</b>\n"
            "Telegram's official program. It pays you back <b>up to {stars_percent}% in Stars</b> "
            "on every payment an invited user makes — again and again, not just once.\n"
            "Its link is in the bot profile: open the bot's card and tap "
            "<b>“Invite friends”</b> (or <b>“My Stars”</b>).\n\n"
            "<b>🎁 2. Free subscription days</b>\n"
            "For everyone who starts the bot for the first time from your link below — "
            "<b>+{bonus_days} day</b> of subscription. Already active? We just add it to your time.\n\n"
            "Invited so far: <b>{invites_count}</b>\n"
            "Days earned: <b>{total_bonus_days}</b>\n\n"
            "<b>Your link:</b>\n"
            "<code>{referral_url}</code>"
        ),
        "pt": (
            "<b>Convide amigos — ganhe duas vezes</b>\n\n"
            "Você tem <b>dois programas rodando ao mesmo tempo.</b>\n\n"
            "<b>💰 1. Stars em cada pagamento</b>\n"
            "Programa oficial do Telegram. Devolve para você <b>até {stars_percent}% em Stars</b> "
            "de cada pagamento de um convidado — sempre, não só uma vez.\n"
            "O link dele está no perfil do bot: abra o cartão do bot e toque em "
            "<b>“Convidar amigos”</b> (ou <b>“Meus Stars”</b>).\n\n"
            "<b>🎁 2. Dias grátis de assinatura</b>\n"
            "Para cada pessoa que iniciar o bot pela primeira vez pelo seu link abaixo — "
            "<b>+{bonus_days} dia</b> de assinatura. Já tem ativa? Somamos ao seu tempo.\n\n"
            "Convidados até agora: <b>{invites_count}</b>\n"
            "Dias acumulados: <b>{total_bonus_days}</b>\n\n"
            "<b>Seu link:</b>\n"
            "<code>{referral_url}</code>"
        ),
        "id": (
            "<b>Undang teman — dapat dua kali</b>\n\n"
            "Anda punya <b>dua program sekaligus.</b>\n\n"
            "<b>💰 1. Stars di setiap pembayaran</b>\n"
            "Program resmi Telegram. Mengembalikan <b>hingga {stars_percent}% dalam Stars</b> "
            "dari setiap pembayaran orang yang diundang — berulang, bukan sekali saja.\n"
            "Tautannya ada di profil bot: buka kartu bot dan ketuk "
            "<b>“Undang teman”</b> (atau <b>“Stars Saya”</b>).\n\n"
            "<b>🎁 2. Hari langganan gratis</b>\n"
            "Untuk setiap orang yang pertama kali menjalankan bot lewat tautan Anda di bawah — "
            "<b>+{bonus_days} hari</b> langganan. Sudah aktif? Kami tambahkan ke sisa waktu.\n\n"
            "Sudah diundang: <b>{invites_count}</b>\n"
            "Hari terkumpul: <b>{total_bonus_days}</b>\n\n"
            "<b>Tautan Anda:</b>\n"
            "<code>{referral_url}</code>"
        ),
    },
    "referral_share_text": {
        "ru": "Запусти Partisans по моей ссылке",
        "en": "Start Partisans with my referral link",
        "pt": "Inicie o Partisans pelo meu link de indicação",
        "id": "Mulai Partisans lewat tautan referral saya",
    },

    # ── Статус подписки ───────────────────────────────────────────────────
    "sub_active": {
        "ru": (
            "✅ <b>Подписка активна</b>\n\n"
            "Тариф: <b>{plan}</b>\n"
            "Действует до: <b>{expires} UTC</b>\n"
            "Автоматизация чатов: <b>{connected}</b>\n\n"
            "Исчезающие фото и видео теперь сохраняются автоматически. Отдыхай — "
            "Partisans на страже."
        ),
        "en": (
            "✅ <b>Subscription active</b>\n\n"
            "Plan: <b>{plan}</b>\n"
            "Valid until: <b>{expires} UTC</b>\n"
            "Chat Automation: <b>{connected}</b>\n\n"
            "Disappearing photos and videos are now saved automatically. Relax — "
            "Partisans is on guard."
        ),
        "pt": (
            "✅ <b>Assinatura ativa</b>\n\n"
            "Plano: <b>{plan}</b>\n"
            "Válido até: <b>{expires} UTC</b>\n"
            "Automação de chats: <b>{connected}</b>\n\n"
            "Fotos e vídeos temporários agora são salvos automaticamente. Relaxe — "
            "o Partisans está de guarda."
        ),
        "id": (
            "✅ <b>Langganan aktif</b>\n\n"
            "Paket: <b>{plan}</b>\n"
            "Berlaku hingga: <b>{expires} UTC</b>\n"
            "Otomatisasi Chat: <b>{connected}</b>\n\n"
            "Foto dan video sementara kini tersimpan otomatis. Santai saja — "
            "Partisans yang berjaga."
        ),
    },
    "sub_inactive": {
        "ru": (
            "<b>У тебя ещё нет подписки</b>\n\n"
            "🎁 <b>Бесплатно уже сейчас:</b> удалённые и изменённые сообщения — "
            "просто подключи бота через <b>Автоматизацию чатов</b>.\n\n"
            "🔓 <b>По подписке:</b> исчезающие фото и видео сохраняются навсегда. "
            "Именно то, что показывают на пару секунд и стирают.\n\n"
            "Оформи за минуту — ниже."
        ),
        "en": (
            "<b>You don't have a subscription yet</b>\n\n"
            "🎁 <b>Free right now:</b> deleted and edited messages — just connect the "
            "bot via <b>Chat Automation</b>.\n\n"
            "🔓 <b>With a subscription:</b> disappearing photos and videos are saved "
            "forever. Exactly what they show for a couple of seconds and wipe.\n\n"
            "Get it in a minute — below."
        ),
        "pt": (
            "<b>Você ainda não tem assinatura</b>\n\n"
            "🎁 <b>Grátis agora:</b> mensagens apagadas e editadas — basta conectar o "
            "bot via <b>Automação de chats</b>.\n\n"
            "🔓 <b>Com assinatura:</b> fotos e vídeos temporários são salvos para "
            "sempre. Justo o que mostram por segundos e apagam.\n\n"
            "Assine em um minuto — abaixo."
        ),
        "id": (
            "<b>Anda belum punya langganan</b>\n\n"
            "🎁 <b>Gratis sekarang:</b> pesan yang dihapus dan diedit — cukup hubungkan "
            "bot lewat <b>Otomatisasi Chat</b>.\n\n"
            "🔓 <b>Dengan langganan:</b> foto dan video sementara tersimpan selamanya. "
            "Persis yang ditampilkan sedetik lalu dihapus.\n\n"
            "Berlangganan dalam satu menit — di bawah."
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
    "method_title": {
        "ru": (
            "🔓 <b>Открой исчезающие фото и видео</b>\n\n"
            "Одноразовое фото исчезает через пару секунд после просмотра — и второго "
            "шанса нет. С подпиской каждое такое фото и видео <b>сохраняется у тебя "
            "навсегда</b> и приходит обычным файлом.\n\n"
            "Настроил один раз — работает в фоне, ничего не нужно нажимать.\n\n"
            "<i>Удалённые и изменённые сообщения остаются бесплатными.</i>\n\n"
            "Выбери способ оплаты 👇"
        ),
        "en": (
            "🔓 <b>Unlock disappearing photos and videos</b>\n\n"
            "A one-time photo vanishes seconds after it's opened — with no second chance. "
            "With a subscription, every such photo and video <b>stays with you forever</b> "
            "and arrives as a regular file.\n\n"
            "Set it up once — it runs in the background, nothing to tap.\n\n"
            "<i>Deleted and edited messages stay free.</i>\n\n"
            "Choose a payment method 👇"
        ),
        "pt": (
            "🔓 <b>Desbloqueie fotos e vídeos que desaparecem</b>\n\n"
            "Uma foto de uso único some segundos após ser aberta — sem segunda chance. "
            "Com a assinatura, cada foto e vídeo desses <b>fica com você para sempre</b> "
            "e chega como um arquivo comum.\n\n"
            "Configure uma vez — funciona em segundo plano, sem tocar em nada.\n\n"
            "<i>Mensagens apagadas e editadas continuam grátis.</i>\n\n"
            "Escolha a forma de pagamento 👇"
        ),
        "id": (
            "🔓 <b>Buka foto dan video yang menghilang</b>\n\n"
            "Foto sekali-pakai lenyap beberapa detik setelah dibuka — tanpa kesempatan kedua. "
            "Dengan langganan, setiap foto dan video seperti itu <b>tersimpan selamanya</b> "
            "dan datang sebagai file biasa.\n\n"
            "Atur sekali — bekerja di latar belakang, tanpa perlu menekan apa pun.\n\n"
            "<i>Pesan yang dihapus dan diedit tetap gratis.</i>\n\n"
            "Pilih metode pembayaran 👇"
        ),
    },
    "plans_title_method": {
        "ru": "<b>Оплата через {method}</b>\n\nВыбери тариф:",
        "en": "<b>Payment via {method}</b>\n\nChoose a plan:",
        "pt": "<b>Pagamento via {method}</b>\n\nEscolha um plano:",
        "id": "<b>Pembayaran via {method}</b>\n\nPilih paket:",
    },
    "btn_method_sbp": {
        "ru": "СБП — рубли",
        "en": "SBP — Russian banks",
        "pt": "SBP — bancos russos",
        "id": "SBP — bank Rusia",
    },
    "sbp_soon": {
        "ru": (
            "<b>Оплата через СБП скоро заработает.</b>\n\n"
            "Мы подключаем приём платежей по Системе быстрых платежей. "
            "Пока оплатить подписку можно через CryptoBot или Telegram Stars."
        ),
        "en": (
            "<b>SBP payments are coming soon.</b>\n\n"
            "We are connecting the Faster Payments System. "
            "For now you can pay with CryptoBot or Telegram Stars."
        ),
        "pt": (
            "<b>Os pagamentos via SBP estarão disponíveis em breve.</b>\n\n"
            "Estamos a ligar o Sistema de Pagamentos Rápidos. "
            "Por enquanto, pode pagar com CryptoBot ou Telegram Stars."
        ),
        "id": (
            "<b>Pembayaran SBP segera hadir.</b>\n\n"
            "Kami sedang menghubungkan Faster Payments System. "
            "Untuk saat ini Anda dapat membayar dengan CryptoBot atau Telegram Stars."
        ),
    },
    "btn_support": {
        "ru": "💬 Поддержка и документы",
        "en": "💬 Support and documents",
        "pt": "💬 Suporte e documentos",
        "id": "💬 Dukungan dan dokumen",
    },
    "support_title": {
        "ru": (
            "<b>Поддержка</b>\n\n"
            "Пиши в любое время: {contact}\n"
            "Обычно отвечаем в течение 24 часов.\n\n"
            "<b>Документы</b>\n"
            "Ниже — Политика конфиденциальности и Пользовательское соглашение "
            "с актуальными тарифами и условиями возврата."
        ),
        "en": (
            "<b>Support</b>\n\n"
            "Write any time: {contact}\n"
            "We usually reply within 24 hours.\n\n"
            "<b>Documents</b>\n"
            "Below are the Privacy Policy and the Terms of Use "
            "with current prices and refund conditions."
        ),
        "pt": (
            "<b>Suporte</b>\n\n"
            "Escreva a qualquer momento: {contact}\n"
            "Normalmente respondemos em 24 horas.\n\n"
            "<b>Documentos</b>\n"
            "Abaixo estão a Política de Privacidade e os Termos de Uso "
            "com os preços atuais e as condições de reembolso."
        ),
        "id": (
            "<b>Dukungan</b>\n\n"
            "Hubungi kapan saja: {contact}\n"
            "Kami biasanya membalas dalam 24 jam.\n\n"
            "<b>Dokumen</b>\n"
            "Di bawah ini adalah Kebijakan Privasi dan Ketentuan Penggunaan "
            "dengan harga terkini dan ketentuan pengembalian dana."
        ),
    },
    "btn_privacy": {
        "ru": "Политика конфиденциальности",
        "en": "Privacy Policy",
        "pt": "Política de Privacidade",
        "id": "Kebijakan Privasi",
    },
    "btn_terms": {
        "ru": "Пользовательское соглашение",
        "en": "Terms of Use",
        "pt": "Termos de Uso",
        "id": "Ketentuan Penggunaan",
    },
    "btn_write_support": {
        "ru": "Написать в поддержку",
        "en": "Message support",
        "pt": "Falar com o suporte",
        "id": "Hubungi dukungan",
    },
    "btn_trial": {
        "ru": "🎁 Попробовать бесплатно",
        "en": "🎁 Try for free",
        "pt": "🎁 Testar grátis",
        "id": "🎁 Coba gratis",
    },
    "trial_activated": {
        "ru": (
            "🎉 <b>Готово! У тебя {days} дня бесплатно.</b>\n\n"
            "Полный доступ, включая перехват исчезающих фото и видео — проверь бота "
            "в деле.\n\n"
            "<b>Один шаг до старта:</b> подключи бота через <b>Настройки → Автоматизация "
            "чатов → Чат-боты</b>, и он сразу начнёт ловить всё в твоих чатах."
        ),
        "en": (
            "🎉 <b>Done! You have {days} days free.</b>\n\n"
            "Full access, including catching disappearing photos and videos — put the "
            "bot to the test.\n\n"
            "<b>One step to start:</b> connect the bot via <b>Settings → Chat Automation "
            "→ Chat Bots</b>, and it will start catching everything in your chats."
        ),
        "pt": (
            "🎉 <b>Pronto! Você tem {days} dias grátis.</b>\n\n"
            "Acesso completo, incluindo capturar fotos e vídeos que desaparecem — "
            "coloque o bot à prova.\n\n"
            "<b>Um passo para começar:</b> conecte o bot via <b>Configurações → Automação "
            "de chats → Chatbots</b>, e ele começará a capturar tudo nos seus chats."
        ),
        "id": (
            "🎉 <b>Selesai! Anda punya {days} hari gratis.</b>\n\n"
            "Akses penuh, termasuk menangkap foto dan video yang menghilang — uji bot "
            "ini.\n\n"
            "<b>Satu langkah untuk mulai:</b> hubungkan bot lewat <b>Pengaturan → "
            "Otomatisasi Chat → Bot Chat</b>, dan ia langsung menangkap semua di chat Anda."
        ),
    },

    # ── Userbot ────────────────────────────────────────────────────────────
    "userbot_title": {
        "ru": (
            "🔓 <b>Последний шаг</b>\n\n"
            "Чтобы ловить исчезающие фото и видео, Telegram должен «видеть» их твоими "
            "глазами — поэтому нужна разовая авторизация твоего аккаунта.\n\n"
            "Нажми кнопку ниже — откроется безопасная форма входа <b>внутри Telegram</b>.\n"
            "🔒 Мы не читаем твою переписку и не пишем от твоего имени. Отключить можно "
            "в один тап в любой момент."
        ),
        "en": (
            "🔓 <b>One last step</b>\n\n"
            "To catch disappearing photos and videos, Telegram has to “see” them through "
            "your eyes — so a one-time authorization of your account is required.\n\n"
            "Tap the button below — a secure sign-in form opens <b>inside Telegram</b>.\n"
            "🔒 We don't read your chats and never message on your behalf. Disconnect in "
            "one tap anytime."
        ),
        "pt": (
            "🔓 <b>Último passo</b>\n\n"
            "Para capturar fotos e vídeos que desaparecem, o Telegram precisa “ver” por "
            "seus olhos — por isso é necessária uma autorização única da sua conta.\n\n"
            "Toque no botão abaixo — um formulário de login seguro abre <b>dentro do "
            "Telegram</b>.\n"
            "🔒 Não lemos suas conversas nem enviamos nada em seu nome. Desconecte com um "
            "toque quando quiser."
        ),
        "id": (
            "🔓 <b>Langkah terakhir</b>\n\n"
            "Untuk menangkap foto dan video yang menghilang, Telegram harus “melihat” lewat "
            "mata Anda — jadi diperlukan otorisasi akun sekali saja.\n\n"
            "Ketuk tombol di bawah — formulir masuk yang aman terbuka <b>di dalam "
            "Telegram</b>.\n"
            "🔒 Kami tidak membaca obrolan Anda dan tidak pernah mengirim atas nama Anda. "
            "Putuskan dengan satu ketukan kapan saja."
        ),
    },
    "btn_open_miniapp": {
        "ru": "🔒 Безопасный вход",
        "en": "🔒 Secure sign-in",
        "pt": "🔒 Entrada segura",
        "id": "🔒 Masuk aman",
    },
    "userbot_active": {
        "ru": (
            "✅ <b>Всё работает</b>\n\n"
            "Исчезающие фото и видео теперь сохраняются автоматически и приходят тебе "
            "обычными файлами. Больше ничего делать не нужно."
        ),
        "en": (
            "✅ <b>All set</b>\n\n"
            "Disappearing photos and videos are now saved automatically and arrive as "
            "regular files. Nothing else to do."
        ),
        "pt": (
            "✅ <b>Tudo pronto</b>\n\n"
            "Fotos e vídeos temporários agora são salvos automaticamente e chegam como "
            "arquivos comuns. Nada mais a fazer."
        ),
        "id": (
            "✅ <b>Semua siap</b>\n\n"
            "Foto dan video sementara kini tersimpan otomatis dan datang sebagai file "
            "biasa. Tidak ada lagi yang perlu dilakukan."
        ),
    },
    "btn_disconnect_userbot": {
        "ru": "Отключить перехват",
        "en": "Disconnect interception",
        "pt": "Desconectar interceptação",
        "id": "Putuskan intersepsi",
    },

    # ── Бизнес-события ────────────────────────────────────────────────────
    # Оформление повторяет журнал действий Telegram: «Имя удалил(а) сообщение:»
    "deleted_notice": {
        "ru": "{name} удалил(а) сообщение:",
        "en": "{name} deleted a message:",
        "pt": "{name} apagou uma mensagem:",
        "id": "{name} menghapus pesan:",
    },
    "edited_notice": {
        "ru": "{name} изменил(а) сообщение:",
        "en": "{name} edited a message:",
        "pt": "{name} editou uma mensagem:",
        "id": "{name} mengedit pesan:",
    },
    "original_message": {
        "ru": "Исходное сообщение",
        "en": "Original message",
        "pt": "Mensagem original",
        "id": "Pesan asli",
    },
    "unknown_sender": {
        "ru": "Неизвестный",
        "en": "Unknown",
        "pt": "Desconhecido",
        "id": "Tidak dikenal",
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
    "not_saved": {
        "ru": "(не сохранено)",
        "en": "(not saved)",
        "pt": "(não salvo)",
        "id": "(tidak tersimpan)",
    },
    "media_unknown": {
        "ru": "[Медиа без текста]",
        "en": "[Media without text]",
        "pt": "[Mídia sem texto]",
        "id": "[Media tanpa teks]",
    },

    # ── Защита от перехвата ───────────────────────────────────────────────
    "btn_protection": {
        "ru": "🛡 Защита от перехвата",
        "en": "🛡 Anti-intercept protection",
        "pt": "🛡 Proteção contra interceptação",
        "id": "🛡 Perlindungan anti-intersepsi",
    },
    "btn_buy_protection": {
        "ru": "Купить защиту",
        "en": "Buy protection",
        "pt": "Comprar proteção",
        "id": "Beli perlindungan",
    },
    "protection_title": {
        "ru": (
            "🛡 <b>Защита Partisans</b>\n\n"
            "Разовая покупка делает тебя <b>невидимым внутри Partisans</b>:\n"
            "• твои одноразовые фото и видео бот не перехватит\n"
            "• твои удалённые и изменённые сообщения не сохраняются и не пересылаются\n"
            "• ты получишь уведомление, если кто-то попытается тебя перехватить\n\n"
            "⚠️ Защита действует <b>только против Partisans</b>. Она не защищает от "
            "скриншотов, съёмки со второго устройства и других ботов.\n\n"
            "Цена: <b>${price}</b> — разово, навсегда."
        ),
        "en": (
            "🛡 <b>Partisans Protection</b>\n\n"
            "A one-time purchase makes you <b>invisible inside Partisans</b>:\n"
            "• the bot won't intercept your one-time photos and videos\n"
            "• your deleted and edited messages are not saved or forwarded\n"
            "• you get notified if someone tries to intercept you\n\n"
            "⚠️ Protection works <b>only against Partisans</b>. It does not protect against "
            "screenshots, a second device, or other bots.\n\n"
            "Price: <b>${price}</b> — one-time, forever."
        ),
        "pt": (
            "🛡 <b>Proteção Partisans</b>\n\n"
            "Uma compra única torna você <b>invisível dentro do Partisans</b>:\n"
            "• o bot não interceptará suas fotos e vídeos temporários\n"
            "• suas mensagens apagadas e editadas não são salvas nem encaminhadas\n"
            "• você é notificado se alguém tentar interceptá-lo\n\n"
            "⚠️ A proteção funciona <b>apenas contra o Partisans</b>. Não protege contra "
            "capturas de tela, um segundo dispositivo ou outros bots.\n\n"
            "Preço: <b>${price}</b> — única, para sempre."
        ),
        "id": (
            "🛡 <b>Perlindungan Partisans</b>\n\n"
            "Pembelian sekali bayar membuat Anda <b>tak terlihat di dalam Partisans</b>:\n"
            "• bot tidak akan mencegat foto dan video sekali-pakai Anda\n"
            "• pesan Anda yang dihapus dan diedit tidak disimpan atau diteruskan\n"
            "• Anda diberi tahu jika seseorang mencoba mencegat Anda\n\n"
            "⚠️ Perlindungan hanya bekerja <b>terhadap Partisans</b>. Tidak melindungi dari "
            "tangkapan layar, perangkat kedua, atau bot lain.\n\n"
            "Harga: <b>${price}</b> — sekali, selamanya."
        ),
    },
    "protection_active": {
        "ru": (
            "🛡 <b>Ты под защитой Partisans.</b>\n\n"
            "Бот игнорирует твои сообщения и одноразовые медиа. "
            "Если тебя попытаются перехватить — мы уведомим."
        ),
        "en": (
            "🛡 <b>You are protected by Partisans.</b>\n\n"
            "The bot ignores your messages and one-time media. "
            "If someone tries to intercept you, we'll notify you."
        ),
        "pt": (
            "🛡 <b>Você está protegido pelo Partisans.</b>\n\n"
            "O bot ignora suas mensagens e mídias temporárias. "
            "Se alguém tentar interceptá-lo, avisaremos."
        ),
        "id": (
            "🛡 <b>Anda dilindungi oleh Partisans.</b>\n\n"
            "Bot mengabaikan pesan dan media sekali-pakai Anda. "
            "Jika seseorang mencoba mencegat Anda, kami akan memberi tahu."
        ),
    },
    "protection_choose_method": {
        "ru": "Выбери способ оплаты защиты:",
        "en": "Choose a payment method for protection:",
        "pt": "Escolha um método de pagamento para a proteção:",
        "id": "Pilih metode pembayaran untuk perlindungan:",
    },
    "protection_pay_crypto": {
        "ru": (
            "<b>Оплата защиты через CryptoBot</b>\n\n"
            "Сумма: <b>${price}</b>\n\n"
            "Нажми «Оплатить», затем вернись и нажми «Я оплатил»."
        ),
        "en": (
            "<b>Protection payment via CryptoBot</b>\n\n"
            "Amount: <b>${price}</b>\n\n"
            "Tap «Pay», then come back and tap «I paid»."
        ),
        "pt": (
            "<b>Pagamento da proteção via CryptoBot</b>\n\n"
            "Valor: <b>${price}</b>\n\n"
            "Toque em «Pagar», depois volte e toque em «Paguei»."
        ),
        "id": (
            "<b>Pembayaran perlindungan via CryptoBot</b>\n\n"
            "Jumlah: <b>${price}</b>\n\n"
            "Ketuk «Bayar», lalu kembali dan ketuk «Saya sudah bayar»."
        ),
    },
    "protection_invoice_title": {
        "ru": "Partisans — Защита",
        "en": "Partisans — Protection",
        "pt": "Partisans — Proteção",
        "id": "Partisans — Perlindungan",
    },
    "protection_invoice_desc": {
        "ru": "Разовая защита от перехвата внутри Partisans",
        "en": "One-time anti-interception protection inside Partisans",
        "pt": "Proteção única contra interceptação dentro do Partisans",
        "id": "Perlindungan sekali-pakai anti-intersepsi di dalam Partisans",
    },
    "protection_activated": {
        "ru": (
            "🛡 <b>Защита активирована.</b>\n\n"
            "Теперь ты невидим внутри Partisans. "
            "Активация может занять несколько минут."
        ),
        "en": (
            "🛡 <b>Protection activated.</b>\n\n"
            "You are now invisible inside Partisans. "
            "Activation may take a few minutes."
        ),
        "pt": (
            "🛡 <b>Proteção ativada.</b>\n\n"
            "Agora você está invisível dentro do Partisans. "
            "A ativação pode levar alguns minutos."
        ),
        "id": (
            "🛡 <b>Perlindungan aktif.</b>\n\n"
            "Sekarang Anda tak terlihat di dalam Partisans. "
            "Aktivasi mungkin memerlukan beberapa menit."
        ),
    },
    "protection_attempt_notice": {
        "ru": "🛡 <b>{name}</b> пытался сохранить твои данные через Partisans — защита сработала, перехват заблокирован.",
        "en": "🛡 <b>{name}</b> tried to capture your data via Partisans — protection kicked in, interception blocked.",
        "pt": "🛡 <b>{name}</b> tentou capturar seus dados via Partisans — a proteção agiu, interceptação bloqueada.",
        "id": "🛡 <b>{name}</b> mencoba menangkap data Anda via Partisans — perlindungan bekerja, intersepsi diblokir.",
    },
    "protection_someone": {
        "ru": "Кто-то",
        "en": "Someone",
        "pt": "Alguém",
        "id": "Seseorang",
    },
    "protection_already": {
        "ru": "Ты уже под защитой.",
        "en": "You are already protected.",
        "pt": "Você já está protegido.",
        "id": "Anda sudah dilindungi.",
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
