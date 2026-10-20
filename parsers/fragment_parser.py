# Парсер для Fragment (Telegram Gift NFT)

import logging
from typing import List, Dict, Optional
from parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class FragmentParser(BaseParser):
    """Парсер для Fragment - основной маркет Telegram Gift NFT"""
    
    def __init__(self, config: dict):
        super().__init__("Fragment", config)
        self.base_url = "https://fragment.com"
        
    async def fetch_lots(self) -> List[Dict]:
        """Получить лоты Gift NFT с Fragment"""
        
        if not self.enabled:
            return []
        
        lots = []
        
        try:
            # Fragment использует GraphQL API
            # Пример запроса для получения Gift NFT на продаже
            
            # URL для Gift NFT marketplace
            url = f"{self.base_url}/api/gifts/marketplace"
            
            # Параметры запроса
            params = {
                "sort": "recent",  # recent, price_asc, price_desc
                "limit": 50
            }
            
            # Пока используем заглушку, так как точный API Fragment требует исследования
            # В реальности нужно будет:
            # 1. Исследовать Network в браузере при открытии fragment.com/gifts
            # 2. Найти API endpoints
            # 3. Реализовать правильные запросы
            
            logger.info(f"Fragment: Fetching lots from {url}")
            
            # TODO: Реализовать реальный запрос к Fragment API
            # data = await self.http_get(url, params=params)
            
            # if data and "gifts" in data:
            #     for gift_data in data["gifts"]:
            #         lot = self.parse_lot_data(gift_data)
            #         if lot:
            #             lots.append(lot)
            
            logger.info(f"Fragment: Found {len(lots)} lots")
            
        except Exception as e:
            logger.error(f"Fragment: Error fetching lots: {e}")
        
        return lots
    
    def parse_lot_data(self, raw_data: dict) -> Optional[Dict]:
        """Парсить данные лота с Fragment"""
        
        try:
            # Пример структуры данных Fragment Gift NFT
            # Нужно адаптировать под реальный формат API
            
            # Извлекаем ID и создаем listing_id
            gift_id = raw_data.get("id")
            listing_id = f"fragment_{gift_id}"
            
            # Информация о подарке
            title = raw_data.get("title", "Unknown Gift")
            collection = raw_data.get("collection", "")
            
            # URL
            url = f"https://t.me/nft/{gift_id}"
            
            # Изображения
            img_url = raw_data.get("image_url", "")
            img_alt_url = raw_data.get("thumbnail_url", img_url)
            
            # Цена
            price_data = raw_data.get("price", {})
            currency = "ton" if price_data.get("currency") == "TON" else "stars"
            price_value = float(price_data.get("amount", 0))
            
            # Конвертация (примерно 1 TON ≈ 150 Stars)
            if currency == "ton":
                price = price_value
                stars = int(price_value * 150)
            else:
                stars = int(price_value)
                price = price_value / 150
            
            # Старая цена (если есть снижение)
            old_price_data = raw_data.get("old_price")
            old_price = None
            old_stars = None
            is_price_drop = False
            
            if old_price_data:
                is_price_drop = True
                if currency == "ton":
                    old_price = float(old_price_data.get("amount", 0))
                    old_stars = int(old_price * 150)
                else:
                    old_stars = int(old_price_data.get("amount", 0))
                    old_price = old_stars / 150
            
            # Атрибуты NFT
            attributes = raw_data.get("attributes", {})
            
            model = None
            if "model" in attributes:
                model = {
                    "name": attributes["model"].get("name", ""),
                    "rarity": attributes["model"].get("rarity"),
                    "tier": attributes["model"].get("tier"),
                    "floor": attributes["model"].get("floor"),
                    "floor_stars": attributes["model"].get("floor_stars")
                }
            
            backdrop = None
            if "backdrop" in attributes:
                backdrop = {
                    "name": attributes["backdrop"].get("name", ""),
                    "rarity": attributes["backdrop"].get("rarity"),
                    "tier": attributes["backdrop"].get("tier"),
                    "floor": attributes["backdrop"].get("floor"),
                    "floor_stars": attributes["backdrop"].get("floor_stars")
                }
            
            pattern = None
            if "pattern" in attributes:
                pattern = {
                    "name": attributes["pattern"].get("name", ""),
                    "rarity": attributes["pattern"].get("rarity"),
                    "tier": attributes["pattern"].get("tier"),
                    "floor": attributes["pattern"].get("floor"),
                    "floor_stars": attributes["pattern"].get("floor_stars")
                }
            
            # Информация о продавце
            seller = raw_data.get("seller", {})
            seller_id = seller.get("id", 0)
            seller_username = seller.get("username", "")
            seller_name = seller.get("name", "")
            seller_avatar = seller.get("photo_url", "")
            seller_premium = seller.get("is_premium", False)
            
            return {
                "listing_id": listing_id,
                "title": title,
                "url": url,
                "collection": collection,
                "img_url": img_url,
                "img_alt_url": img_alt_url,
                "currency": currency,
                "price": price,
                "stars": stars,
                "old_price": old_price,
                "old_stars": old_stars,
                "is_price_drop": is_price_drop,
                "model": model,
                "backdrop": backdrop,
                "pattern": pattern,
                "seller_id": seller_id,
                "seller_username": seller_username,
                "seller_name": seller_name,
                "seller_avatar": seller_avatar,
                "seller_premium": seller_premium,
                "source": "fragment"
            }
            
        except Exception as e:
            logger.error(f"Fragment: Error parsing lot data: {e}")
            return None
    
    async def fetch_seller_info(self, seller_id: int) -> Optional[Dict]:
        """Получить информацию о продавце с Fragment"""
        
        try:
            # TODO: Реализовать запрос профиля пользователя
            # url = f"{self.base_url}/api/user/{seller_id}"
            # data = await self.http_get(url)
            
            # if data:
            #     return {
            #         "level": data.get("level"),
            #         "nft_count": data.get("nft_count"),
            #         "lots_count": data.get("active_lots"),
            #         "dm_cost": data.get("dm_cost_stars", 0),
            #         ...
            #     }
            
            return None
            
        except Exception as e:
            logger.error(f"Fragment: Error fetching seller info: {e}")
            return None
