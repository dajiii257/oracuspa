# Базовый класс для парсеров

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Базовый класс для парсеров маркетов"""
    
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", False)
        self.api_url = config.get("api_url")
        self.api_key = config.get("api_key")
        
    @abstractmethod
    async def fetch_lots(self) -> List[Dict]:
        """
        Получить лоты с маркета
        
        Returns:
            List[Dict]: Список лотов в стандартном формате
        """
        pass
    
    async def fetch_seller_info(self, seller_id: int) -> Optional[Dict]:
        """
        Получить информацию о продавце
        
        Returns:
            Dict: Информация о продавце
        """
        return None
    
    def parse_lot_data(self, raw_data: dict) -> Optional[Dict]:
        """
        Парсить сырые данные лота в стандартный формат
        
        Args:
            raw_data: Сырые данные от API маркета
            
        Returns:
            Dict со стандартными полями:
            {
                "listing_id": str,
                "title": str,
                "url": str,
                "collection": str,
                "img_url": str,
                "img_alt_url": str,
                "currency": "ton" | "stars",
                "price": float,
                "stars": int,
                "old_price": float,
                "old_stars": int,
                "is_price_drop": bool,
                "model": {"name": str, "rarity": float, "tier": str, "floor": float, "floor_stars": int},
                "backdrop": {...},
                "pattern": {...},
                "seller_id": int,
                "seller_username": str,
                "seller_name": str,
                "seller_avatar": str,
                "seller_premium": bool
            }
        """
        return None
    
    async def http_get(self, url: str, headers: dict = None) -> Optional[dict]:
        """HTTP GET запрос"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                        return None
        except Exception as e:
            logger.error(f"{self.name}: Error fetching {url}: {e}")
            return None
    
    async def http_post(self, url: str, data: dict, headers: dict = None) -> Optional[dict]:
        """HTTP POST запрос"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                        return None
        except Exception as e:
            logger.error(f"{self.name}: Error posting to {url}: {e}")
            return None
