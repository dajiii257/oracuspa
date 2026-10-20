# Конфигурация Ocerao Tracker Bot

# ============ TELEGRAM BOT ============
# Получите токен у @BotFather
BOT_TOKEN = "8809723382:AAFuCuRGQYKe_tvEgzLGZ1VagC8RDtWLpFc"

# ID администраторов (список Telegram ID)
# Узнать свой ID можно у @userinfobot
ADMIN_IDS = [
    8307076618,  # Замените на свой Telegram ID
    192237320,
    6655077013,
]

# Webhook настройки (оставьте None для polling)
WEBHOOK_URL = "https://oracuspars555.tech"  # Или None для polling
WEBHOOK_PATH = "/webhook"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8080

# ============ БАЗА ДАННЫХ ============
# SQLite для начала, потом можно переключить на PostgreSQL
DATABASE_URL = "sqlite:///ocerao_tracker.db"
# Для PostgreSQL: "postgresql://user:password@localhost/ocerao_tracker"

# ============ ПОДПИСКА И ОПЛАТА ============
# Тарифы (цены в Telegram Stars)
TARIFFS = {
    "1day": {
        "title": "1 день",
        "duration_seconds": 86400,  # 1 день
        "price_stars": 100,
        "price_ton": None,  # Опционально, если нужна оплата TON
    },
    "30days": {
        "title": "30 дней", 
        "duration_seconds": 2592000,  # 30 дней
        "price_stars": 300,
        "price_ton": None,
    },
    "forever": {
        "title": "Навсегда",
        "duration_seconds": None,  # Бессрочно
        "price_stars": 1000,
        "price_ton": None,
    }
}

# Пробный период (в секундах)
TRIAL_DURATION = 600  # 10 минут
TRIAL_MESSAGE = "10 минут бесплатно"

# Реферальная программа
REFERRAL_ENABLED = True
REFERRAL_BONUS_SECONDS = 21600  # 6 часов

# ============ ПАРСЕРЫ МАРКЕТОВ ============
# Интервал парсинга (в секундах)
PARSE_INTERVAL = 60  # Каждую минуту

# Маркеты Gift NFT
MARKETS = {
    "telegram": {
        "enabled": True,
        "api_url": "https://api.telegram.org/nft",  # Пример
    },
    "fragment": {
        "enabled": True,
        "api_url": "https://fragment.com/api",
        "api_key": None,  # Если требуется
    },
    "tonnel": {
        "enabled": True,
        "api_url": None,  # URL API если есть
    },
    "portals": {
        "enabled": True,
        "api_url": None,
    },
    "mrkt": {
        "enabled": True,
        "api_url": None,
    },
    "getgems": {
        "enabled": True,
        "api_url": "https://api.getgems.io",
        "api_key": None,
    }
}

# ============ ТРЕКЕР ============
# Максимальное количество лотов в пачке
MAX_BATCH_SIZE = 10

# Время хранения "занятых" продавцов (чтобы не выдавать повторно)
CLAIMED_SELLER_TTL = 3600  # 1 час

# Редкие разделы: время накопления лотов
RARE_SECTION_ACCUMULATION = 10800  # 3 часа

# ============ MINI APP (FRONTEND) ============
# URL где размещен фронтенд
WEBAPP_URL = "https://oracuspars555.tech"  # Ваш домен

# Путь к статическим файлам фронтенда
FRONTEND_PATH = "frontend"

# ============ API ============
# CORS настройки
CORS_ORIGINS = ["*"]  # В продакшене укажите конкретные домены

# Rate limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_PER_MINUTE = 60

# ============ ЛОГИРОВАНИЕ ============
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "ocerao_tracker.log"

# ============ ДОПОЛНИТЕЛЬНО ============
# Канал для обязательной подписки (опционально)
REQUIRED_CHANNEL = None  # Например: "@your_channel"
REQUIRED_CHANNEL_ID = None  # ID канала

# Поддержка
SUPPORT_USERNAME = None  # Например: "@support"

# Промокоды (можно добавлять через админ-панель)
PROMO_CODES = {
    # "PROMO2024": {
    #     "duration_seconds": 2592000,  # 30 дней
    #     "uses_left": 100,
    # }
}
