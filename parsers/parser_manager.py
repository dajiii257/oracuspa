# Менеджер парсеров - координирует работу всех парсеров

import logging
import asyncio
from typing import List, Dict
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import config
from database import AsyncSessionLocal
from database.models import Lot, SellerCache, Section
from parsers.fragment_parser import FragmentParser
from parsers.telegram_parser import TelegramParser
from parsers.getgems_parser import GetgemsParser

logger = logging.getLogger(__name__)


class ParserManager:
    """Менеджер для управления всеми парсерами"""
    
    def __init__(self):
        self.parsers = []
        self.running = False
        
        # Инициализируем парсеры
        if config.MARKETS.get("fragment", {}).get("enabled"):
            self.parsers.append(FragmentParser(config.MARKETS["fragment"]))
        
        if config.MARKETS.get("telegram", {}).get("enabled"):
            self.parsers.append(TelegramParser(config.MARKETS["telegram"]))
        
        if config.MARKETS.get("getgems", {}).get("enabled"):
            self.parsers.append(GetgemsParser(config.MARKETS["getgems"]))
        
        # TODO: Добавить парсеры для Tonnel, Portals, MRKT
        
        logger.info(f"Initialized {len(self.parsers)} parsers")
    
    async def start(self):
        """Запустить парсинг в фоновом режиме"""
        self.running = True
        logger.info("Parser manager started")
        
        while self.running:
            try:
                await self.parse_all_markets()
                await asyncio.sleep(config.PARSE_INTERVAL)
            except Exception as e:
                logger.error(f"Error in parser loop: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        """Остановить парсинг"""
        self.running = False
        logger.info("Parser manager stopped")
    
    async def parse_all_markets(self):
        """Запустить парсинг всех маркетов"""
        logger.info("Starting market parsing cycle")
        
        all_lots = []
        
        # Параллельно парсим все маркеты
        tasks = [parser.fetch_lots() for parser in self.parsers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Parser {self.parsers[i].name} failed: {result}")
            elif result:
                all_lots.extend(result)
                logger.info(f"{self.parsers[i].name}: fetched {len(result)} lots")
        
        logger.info(f"Total lots fetched: {len(all_lots)}")
        
        # Сохраняем лоты в БД
        if all_lots:
            await self.save_lots(all_lots)
        
        # Обновляем статистику разделов
        await self.update_sections_stats()
    
    async def save_lots(self, lots_data: List[Dict]):
        """Сохранить лоты в базу данных"""
        async with AsyncSessionLocal() as session:
            saved_count = 0
            updated_count = 0
            
            for lot_data in lots_data:
                try:
                    # Проверяем, есть ли уже такой лот
                    result = await session.execute(
                        select(Lot).where(Lot.listing_id == lot_data["listing_id"])
                    )
                    existing_lot = result.scalar_one_or_none()
                    
                    if existing_lot:
                        # Обновляем существующий лот
                        # Проверяем снижение цены
                        if lot_data.get("currency") == "ton":
                            if existing_lot.price and lot_data.get("price") < existing_lot.price:
                                lot_data["old_price"] = existing_lot.price
                                lot_data["old_stars"] = existing_lot.stars
                                lot_data["is_price_drop"] = True
                        
                        # Обновляем поля
                        for key, value in lot_data.items():
                            if hasattr(existing_lot, key):
                                setattr(existing_lot, key, value)
                        
                        existing_lot.updated_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Создаем новый лот
                        lot = Lot(
                            listing_id=lot_data["listing_id"],
                            title=lot_data.get("title", ""),
                            url=lot_data.get("url", ""),
                            collection=lot_data.get("collection"),
                            img_url=lot_data.get("img_url"),
                            img_alt_url=lot_data.get("img_alt_url"),
                            currency=lot_data.get("currency", "ton"),
                            price=lot_data.get("price"),
                            stars=lot_data.get("stars"),
                            old_price=lot_data.get("old_price"),
                            old_stars=lot_data.get("old_stars"),
                            is_price_drop=lot_data.get("is_price_drop", False),
                            model=lot_data.get("model"),
                            backdrop=lot_data.get("backdrop"),
                            pattern=lot_data.get("pattern"),
                            seller_id=lot_data.get("seller_id", 0),
                            seller_username=lot_data.get("seller_username", ""),
                            seller_name=lot_data.get("seller_name", ""),
                            seller_avatar=lot_data.get("seller_avatar"),
                            seller_premium=lot_data.get("seller_premium", False),
                            is_active=True,
                            is_taken=False,
                            caught_at=datetime.utcnow()
                        )
                        session.add(lot)
                        saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving lot {lot_data.get('listing_id')}: {e}")
                    continue
            
            await session.commit()
            logger.info(f"Saved {saved_count} new lots, updated {updated_count} lots")
    
    async def update_sections_stats(self):
        """Обновить статистику разделов"""
        async with AsyncSessionLocal() as session:
            # Получаем все активные разделы
            result = await session.execute(
                select(Section).where(Section.is_active == True)
            )
            sections = result.scalars().all()
            
            for section in sections:
                # Подсчитываем лоты, подходящие под фильтры раздела
                # TODO: Реализовать фильтрацию по filters раздела
                
                # Пока просто обновляем статистику
                result = await session.execute(
                    select(Lot).where(
                        Lot.is_active == True,
                        Lot.is_taken == False
                    )
                )
                all_lots = result.scalars().all()
                
                section.ready_count = min(len(all_lots), 99)
                section.rate = len(all_lots)
            
            await session.commit()
    
    async def fetch_seller_info(self, seller_id: int) -> Dict:
        """Получить информацию о продавце со всех доступных источников"""
        
        # Проверяем кэш
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(SellerCache).where(SellerCache.seller_id == seller_id)
            )
            cached = result.scalar_one_or_none()
            
            # Если в кэше свежие данные (< 1 часа), возвращаем их
            if cached and (datetime.utcnow() - cached.updated_at).seconds < 3600:
                return {
                    "level": cached.level,
                    "nft_count": cached.nft_count,
                    "lots_count": cached.lots_count,
                    "dm_cost": cached.dm_cost,
                    "is_girl": cached.is_girl,
                    "is_anime": cached.is_anime,
                    "is_fancy": cached.is_fancy,
                    "is_trader": cached.is_trader,
                    "is_anon": cached.is_anon,
                    "one_username": cached.one_username
                }
        
        # Запрашиваем у парсеров
        for parser in self.parsers:
            info = await parser.fetch_seller_info(seller_id)
            if info:
                # Сохраняем в кэш
                await self.cache_seller_info(seller_id, info)
                return info
        
        return {}
    
    async def cache_seller_info(self, seller_id: int, info: Dict):
        """Сохранить информацию о продавце в кэш"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(SellerCache).where(SellerCache.seller_id == seller_id)
            )
            cached = result.scalar_one_or_none()
            
            if cached:
                # Обновляем
                for key, value in info.items():
                    if hasattr(cached, key):
                        setattr(cached, key, value)
                cached.updated_at = datetime.utcnow()
            else:
                # Создаем
                cached = SellerCache(
                    seller_id=seller_id,
                    **info
                )
                session.add(cached)
            
            await session.commit()


# Глобальный экземпляр менеджера
parser_manager = ParserManager()
