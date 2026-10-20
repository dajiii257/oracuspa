# Аутентификация через Telegram WebApp

import hmac
import hashlib
from urllib.parse import parse_qs
from typing import Optional, Dict
import logging

import config

logger = logging.getLogger(__name__)


def verify_telegram_webapp_data(init_data: str) -> Optional[Dict]:
    """
    Верифицировать данные от Telegram WebApp
    
    Args:
        init_data: initData от Telegram WebApp
        
    Returns:
        Dict с данными пользователя или None если проверка не прошла
    """
    
    try:
        # Парсим init_data
        parsed = parse_qs(init_data)
        
        # Извлекаем hash
        received_hash = parsed.get('hash', [None])[0]
        if not received_hash:
            logger.warning("No hash in init_data")
            return None
        
        # Удаляем hash из данных для проверки
        data_check_string_parts = []
        for key in sorted(parsed.keys()):
            if key != 'hash':
                value = parsed[key][0]
                data_check_string_parts.append(f"{key}={value}")
        
        data_check_string = '\n'.join(data_check_string_parts)
        
        # Создаем секретный ключ из bot token
        secret_key = hmac.new(
            "WebAppData".encode(),
            config.BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()
        
        # Вычисляем hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Проверяем hash
        if calculated_hash != received_hash:
            logger.warning("Invalid hash in init_data")
            return None
        
        # Извлекаем данные пользователя
        user_data_str = parsed.get('user', [None])[0]
        if not user_data_str:
            logger.warning("No user data in init_data")
            return None
        
        import json
        user_data = json.loads(user_data_str)
        
        return user_data
        
    except Exception as e:
        logger.error(f"Error verifying Telegram data: {e}")
        return None
