# Парсер для Getgems (TON NFT marketplace)

import logging
from typing import List, Dict, Optional
from parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class GetgemsParser(BaseParser):
    """Парсер для Getgems - маркет TON NFT"""
    
    def __init__(self, config: dict):
        super().__init__("Getgems", config)
        self.api_base = self.api_url or "https://api.getgems.io"
        
    async def fetch_lots(self) -> List[Dict]:
        """Получить Gift NFT лоты с Getgems"""
        
        if not self.enabled:
            return []
        
        lots = []
        
        try:
            # Getgems GraphQL API
            # Фильтруем только Telegram Gift NFT коллекции
            
            url = f"{self.api_base}/graphql"
            
            # GraphQL запрос для Gift NFT
            query = """
            query GetGiftListings($limit: Int, $offset: Int) {
                nftItems(
                    filter: {
                        collections: ["telegram_gifts"],
                        saleType: SALE
                    }
                    limit: $limit
                    offset: $offset
                    orderBy: PRICE_ASC
                ) {
                    items {
                        id
                        name
                        image
                        owner {
                            address
                            name
                        }
                        sale {
                            price
                            currency
                        }
                        attributes {
                            trait_type
                            value
                        }
                    }
                }
            }
            """
            
            variables = {
                "limit": 50,
                "offset": 0
            }
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            # TODO: Реализовать реальный запрос
            # data = await self.http_post(url, {
            #     "query": query,
            #     "variables": variables
            # }, headers=headers)
            
            # if data and "data" in data:
            #     items = data["data"].get("nftItems", {}).get("items", [])
            #     for item in items:
            #         lot = self.parse_lot_data(item)
            #         if lot:
            #             lots.append(lot)
            
            logger.info(f"Getgems: Found {len(lots)} Gift NFT lots")
            
        except Exception as e:
            logger.error(f"Getgems: Error fetching lots: {e}")
        
        return lots
    
    def parse_lot_data(self, raw_data: dict) -> Optional[Dict]:
        """Парсить данные NFT с Getgems"""
        
        try:
            nft_id = raw_data.get("id")
            listing_id = f"getgems_{nft_id}"
            
            # Название и изображение
            title = raw_data.get("name", "")
            img_url = raw_data.get("image", "")
            
            # Цена
            sale = raw_data.get("sale", {})
            price_ton = float(sale.get("price", 0)) / 1e9  # Конвертация из nanoTON
            price_stars = int(price_ton * 150)
            
            # Атрибуты
            attributes = raw_data.get("attributes", [])
            model = None
            backdrop = None
            pattern = None
            
            for attr in attributes:
                trait = attr.get("trait_type", "").lower()
                value = attr.get("value", "")
                
                if "model" in trait:
                    model = {"name": value}
                elif "backdrop" in trait or "background" in trait:
                    backdrop = {"name": value}
                elif "pattern" in trait:
                    pattern = {"name": value}
            
            # Владелец (продавец)
            owner = raw_data.get("owner", {})
            owner_address = owner.get("address", "")
            owner_name = owner.get("name", owner_address[:8])
            
            return {
                "listing_id": listing_id,
                "title": title,
                "url": f"https://getgems.io/nft/{nft_id}",
                "collection": "Telegram Gifts",
                "img_url": img_url,
                "img_alt_url": img_url,
                "currency": "ton",
                "price": price_ton,
                "stars": price_stars,
                "model": model,
                "backdrop": backdrop,
                "pattern": pattern,
                "seller_username": owner_name,
                "seller_name": owner_name,
                "source": "getgems"
            }
            
        except Exception as e:
            logger.error(f"Getgems: Error parsing lot: {e}")
            return None
