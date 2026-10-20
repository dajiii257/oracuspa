# Пример конфигурации Ocerao Tracker Bot
# Скопируйте этот файл в config.py и заполните своими данными

# ============ TELEGRAM BOT ============
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Получите у @BotFather

# ID администраторов (список Telegram ID)
ADMIN_IDS = [
    123456789,  # Узнайте свой ID у @userinfobot
]

# Webhook настройки (или None для polling)
WEBHOOK_URL = None  # "https://yourdomain.com" для webhook
WEBHOOK_PATH = "/webhook"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8080

# ============ БАЗА ДАННЫХ ============
DATABASE_URL = "sqlite:///ocerao_tracker.db"
# Для PostgreSQL: "postgresql://user:password@localhost/ocerao_tracker"

# ============ ПОДПИСКА И ОПЛАТА ============
TARIFFS = {
    "1day": {
        "title": "1 день",
        "duration_seconds": 86400,
        "price_stars": 100,
        "price_ton": None,
    },
    "30days": {
        "title": "30 дней", 
        "duration_seconds": 2592000,
        "price_stars": 300,
        "price_ton": None,
    },
    "forever": {
        "title": "Навсегда",
        "duration_seconds": None,
        "price_stars": 1000,
        "price_ton": None,
    }
}

TRIAL_DURATION = 600  # 10 минут
TRIAL_MESSAGE = "10 минут бесплатно"

REFERRAL_ENABLED = True
REFERRAL_BONUS_SECONDS = 21600  # 6 часов

# ============ ПАРСЕРЫ МАРКЕТОВ ============
PARSE_INTERVAL = 60

MARKETS = {
    "telegram": {
        "enabled": True,
        "api_url": "https://api.telegram.org/nft",
    },
    "fragment": {
        "enabled": True,
        "api_url": "https://fragment.com/api",
        "api_key": None,
    },
    "tonnel": {
        "enabled": True,
        "api_url": None,
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
MAX_BATCH_SIZE = 10
CLAIMED_SELLER_TTL = 3600
RARE_SECTION_ACCUMULATION = 10800

# ============ MINI APP (FRONTEND) ============
WEBAPP_URL = "http://localhost:8080"  # Для локальной разработки
# WEBAPP_URL = "https://yourdomain.com"  # Для продакшена

FRONTEND_PATH = "frontend"

# ============ API ============
CORS_ORIGINS = ["*"]
RATE_LIMIT_ENABLED = True
RATE_LIMIT_PER_MINUTE = 60

# ============ ЛОГИРОВАНИЕ ============
LOG_LEVEL = "INFO"
LOG_FILE = "ocerao_tracker.log"

# ============ ДОПОЛНИТЕЛЬНО ============
REQUIRED_CHANNEL = None
REQUIRED_CHANNEL_ID = None
SUPPORT_USERNAME = None

PROMO_CODES = {}
