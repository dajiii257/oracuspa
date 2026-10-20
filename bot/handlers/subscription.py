# Обработчики подписки

import logging
from datetime import datetime
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = Router()


# Дополнительные хэндлеры для подписки можно добавить сюда
