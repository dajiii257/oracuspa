# Менеджер подписок

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User


async def check_and_grant_subscription(session: AsyncSession, user: User) -> bool:
    """
    Проверить и обновить статус подписки пользователя
    
    Returns:
        bool: True если есть активная подписка, False если нет
    """
    # Админы всегда имеют доступ
    if user.is_admin:
        return True
    
    # Навсегда
    if user.subscription_forever:
        user.subscription_active = True
        await session.commit()
        return True
    
    # Проверяем срок подписки
    if user.subscription_until:
        if user.subscription_until > datetime.utcnow():
            user.subscription_active = True
            await session.commit()
            return True
        else:
            # Подписка истекла
            user.subscription_active = False
            await session.commit()
            return False
    
    # Нет подписки
    user.subscription_active = False
    await session.commit()
    return False


async def grant_subscription(
    session: AsyncSession,
    user: User,
    duration_seconds: int = None,
    forever: bool = False
) -> None:
    """
    Выдать подписку пользователю
    
    Args:
        session: Сессия БД
        user: Пользователь
        duration_seconds: Длительность в секундах (None если forever=True)
        forever: Выдать навсегда
    """
    from datetime import timedelta
    
    if forever:
        user.subscription_forever = True
        user.subscription_active = True
        user.subscription_until = None
    elif duration_seconds:
        if user.subscription_active and user.subscription_until and user.subscription_until > datetime.utcnow():
            # Продление - добавляем к остатку
            user.subscription_until += timedelta(seconds=duration_seconds)
        else:
            # Новая подписка
            user.subscription_until = datetime.utcnow() + timedelta(seconds=duration_seconds)
        
        user.subscription_active = True
    
    await session.commit()
