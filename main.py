# Главный файл для запуска Ocerao Tracker

import asyncio
import logging
import signal
from concurrent.futures import ThreadPoolExecutor

import config
from bot.main import bot, dp
from backend.main import app
from parsers.parser_manager import parser_manager
from database import init_db

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OceraoTracker:
    """Главный класс приложения"""
    
    def __init__(self):
        self.tasks = []
        self.running = False
    
    async def start(self):
        """Запустить все компоненты"""
        logger.info("=" * 50)
        logger.info("Starting Ocerao Tracker")
        logger.info("=" * 50)
        
        # Инициализируем базу данных
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized ✓")
        
        # Создаем начальные разделы, если их нет
        await self.create_default_sections()
        
        self.running = True
        
        # Запускаем компоненты параллельно
        self.tasks = [
            asyncio.create_task(self.run_bot(), name="bot"),
            asyncio.create_task(self.run_api(), name="api"),
            asyncio.create_task(self.run_parser(), name="parser"),
        ]
        
        logger.info("All components started ✓")
        logger.info("=" * 50)
        
        # Ждем завершения всех задач
        await asyncio.gather(*self.tasks, return_exceptions=True)
    
    async def stop(self):
        """Остановить все компоненты"""
        logger.info("Stopping Ocerao Tracker...")
        self.running = False
        
        # Останавливаем парсер
        parser_manager.stop()
        
        # Отменяем все задачи
        for task in self.tasks:
            if not task.done():
                task.cancel()
        
        # Ждем завершения
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
        logger.info("Ocerao Tracker stopped")
    
    async def run_bot(self):
        """Запустить Telegram бота"""
        try:
            logger.info("Starting Telegram Bot...")
            await dp.start_polling(bot, skip_updates=True)
        except asyncio.CancelledError:
            logger.info("Bot task cancelled")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            raise
    
    async def run_api(self):
        """Запустить FastAPI сервер"""
        try:
            logger.info(f"Starting API server on {config.WEBAPP_HOST}:{config.WEBAPP_PORT}...")
            import uvicorn
            
            config_uvicorn = uvicorn.Config(
                app,
                host=config.WEBAPP_HOST,
                port=config.WEBAPP_PORT,
                log_level=config.LOG_LEVEL.lower()
            )
            server = uvicorn.Server(config_uvicorn)
            await server.serve()
        except asyncio.CancelledError:
            logger.info("API task cancelled")
        except Exception as e:
            logger.error(f"API error: {e}")
            raise
    
    async def run_parser(self):
        """Запустить парсеры маркетов"""
        try:
            logger.info("Starting market parsers...")
            await parser_manager.start()
        except asyncio.CancelledError:
            logger.info("Parser task cancelled")
        except Exception as e:
            logger.error(f"Parser error: {e}")
            raise
    
    async def create_default_sections(self):
        """Создать разделы по умолчанию"""
        from database import AsyncSessionLocal
        from database.models import Section
        from sqlalchemy import select
        
        default_sections = [
            {
                "id": 1,
                "name": "Ширпы до 10 TON",
                "hint": "Лоты дешевле 10 TON и снижения цены",
                "icon": "cart",
                "is_rare": False,
                "filters": {"max_ton": 10.0, "events": "all"}
            },
            {
                "id": 2,
                "name": "Дорогие от 10 TON",
                "hint": "Лоты от 10 TON и снижения цены",
                "icon": "gem",
                "is_rare": False,
                "filters": {"min_ton": 10.0, "events": "all"}
            },
            {
                "id": 4,
                "name": "Шрифты",
                "hint": "Продавцы с именем шрифтом",
                "icon": "pen",
                "is_rare": False,
                "filters": {"fancy": True}
            },
            {
                "id": 5,
                "name": "Черный фон",
                "hint": "Black и Onyx Black любой коллекции",
                "icon": "moon",
                "is_rare": True,
                "filters": {"backdrops": ["Black", "Onyx Black"]}
            },
            {
                "id": 6,
                "name": "Нищуки",
                "hint": "ЛС бесплатно, мало NFT и лотов, низкий рейт, не трейдер",
                "icon": "coin",
                "is_rare": False,
                "filters": {
                    "free_dm": True,
                    "one_username": True,
                    "no_anon": True,
                    "no_trader": True,
                    "nft_max": 5,
                    "level_max": 2,
                    "max_lots": 2
                }
            },
            {
                "id": 0,
                "name": "Свой раздел",
                "hint": "",
                "icon": "sliders",
                "is_custom": True,
                "filters": {}
            }
        ]
        
        async with AsyncSessionLocal() as session:
            for section_data in default_sections:
                result = await session.execute(
                    select(Section).where(Section.id == section_data["id"])
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    section = Section(**section_data)
                    session.add(section)
                    logger.info(f"Created section: {section_data['name']}")
            
            await session.commit()


async def main():
    """Главная функция"""
    tracker = OceraoTracker()
    
    # Обработка сигналов для graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}")
        asyncio.create_task(tracker.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await tracker.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        await tracker.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
