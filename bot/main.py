# Telegram Bot главный файл

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message, 
    KeyboardButton, 
    ReplyKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    PreCheckoutQuery,
    LabeledPrice,
)
from aiogram.enums import ParseMode
from datetime import datetime, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import config
from database import init_db, AsyncSessionLocal
from database.models import User, Payment
from bot.keyboards import get_main_menu
from bot.handlers import subscription, payment
from utils.subscription_manager import check_and_grant_subscription

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

# Инициализация бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def get_or_create_user(session: AsyncSession, telegram_user) -> User:
    """Получить или создать пользователя"""
    result = await session.execute(
        select(User).where(User.id == telegram_user.id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        # Создаем нового пользователя
        user = User(
            id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            is_admin=telegram_user.id in config.ADMIN_IDS,
            referral_code=f"ref_{telegram_user.id}",
            preferences={
                "template": "",
                "price_on": False,
                "price_mode": "pct",
                "price_value": 10.0,
                "link": "",
                "batch": 5,
                "haptics": True,
                "fullscreen": False,
                "notify": True,
                "custom": {}
            }
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.info(f"New user created: {user.id} (@{user.username})")
    else:
        # Обновляем информацию
        user.username = telegram_user.username
        user.first_name = telegram_user.first_name
        user.last_name = telegram_user.last_name
        user.last_activity = datetime.utcnow()
        await session.commit()
    
    return user


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""
    async with AsyncSessionLocal() as session:
        user = await get_or_create_user(session, message.from_user)
        
        # Проверка реферальной ссылки
        args = message.text.split()
        if len(args) > 1 and args[1].startswith("ref_"):
            referrer_id = int(args[1].replace("ref_", ""))
            if referrer_id != user.id and not user.referrer_id:
                user.referrer_id = referrer_id
                # Увеличиваем счетчик приглашенных у реферера
                await session.execute(
                    update(User)
                    .where(User.id == referrer_id)
                    .values(referrals_invited=User.referrals_invited + 1)
                )
                await session.commit()
                logger.info(f"User {user.id} invited by {referrer_id}")
        
        # Проверяем подписку
        has_access = user.is_admin or user.subscription_active
        
        if not has_access and not user.trial_used:
            # Даем пробный период
            trial_end = datetime.utcnow() + timedelta(seconds=config.TRIAL_DURATION)
            user.subscription_active = True
            user.subscription_until = trial_end
            user.trial_used = True
            await session.commit()
            
            await message.answer(
                f"🎉 <b>Добро пожаловать в Ocerao Tracker!</b>\n\n"
                f"✨ Трекер лотов маркета подарков: занял продавца, и он только твой\n\n"
                f"🎁 Тебе дается <b>{config.TRIAL_MESSAGE}</b> пробного доступа\n\n"
                f"Открой трекер и начни поиск! 👇",
                reply_markup=get_main_menu(has_access=True)
            )
        elif has_access:
            await message.answer(
                f"👋 С возвращением, <b>{user.first_name or 'друг'}</b>!\n\n"
                f"Трекер готов к работе",
                reply_markup=get_main_menu(has_access=True)
            )
        else:
            await message.answer(
                f"👋 <b>Ocerao Tracker</b>\n\n"
                f"🔍 Свои продавцы, никто не перебивает\n"
                f"🔥 Новые лоты и снижения цен сразу\n"
                f"🎨 Рейт, NFT и флоры в каждой карточке\n\n"
                f"Для работы нужна подписка 👇",
                reply_markup=get_main_menu(has_access=False)
            )


@dp.message(F.text == "🚀 Открыть трекер")
async def open_tracker(message: Message):
    """Открыть MiniApp трекер"""
    async with AsyncSessionLocal() as session:
        user = await get_or_create_user(session, message.from_user)
        
        # Проверяем доступ
        has_access = await check_and_grant_subscription(session, user)
        
        if not has_access:
            await message.answer(
                "❌ У тебя нет активной подписки\n\n"
                "Оформи подписку, чтобы пользоваться трекером",
                reply_markup=get_main_menu(has_access=False)
            )
            return
        
        # Отправляем кнопку с WebApp
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🎯 Открыть трекер",
                web_app=WebAppInfo(url=f"{config.WEBAPP_URL}/tracker-app/")
            )]
        ])
        
        await message.answer(
            "🚀 <b>Трекер готов!</b>\n\n"
            "Нажми на кнопку ниже, чтобы открыть приложение",
            reply_markup=keyboard
        )


@dp.message(F.text == "💎 Продлить")
async def show_subscription(message: Message):
    """Показать тарифы подписки"""
    async with AsyncSessionLocal() as session:
        user = await get_or_create_user(session, message.from_user)
        
        tariff_buttons = []
        for code, tariff in config.TARIFFS.items():
            tariff_buttons.append([
                InlineKeyboardButton(
                    text=f"{tariff['title']} - {tariff['price_stars']} ⭐",
                    callback_data=f"buy_{code}"
                )
            ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=tariff_buttons)
        
        await message.answer(
            "💎 <b>Выбери срок подписки:</b>\n\n"
            "Оплата производится в Telegram Stars ⭐",
            reply_markup=keyboard
        )


@dp.message(F.text == "📊 Моя подписка")
async def my_subscription(message: Message):
    """Информация о подписке"""
    async with AsyncSessionLocal() as session:
        user = await get_or_create_user(session, message.from_user)
        
        if user.is_admin:
            text = (
                "👑 <b>Доступ навсегда</b>\n\n"
                "Ты администратор, трекер открыт без ограничений"
            )
        elif user.subscription_forever:
            text = (
                "✨ <b>Подписка навсегда</b>\n\n"
                "Продлевать не нужно, трекер всегда доступен"
            )
        elif user.subscription_active and user.subscription_until:
            days_left = (user.subscription_until - datetime.utcnow()).days
            text = (
                f"✅ <b>Подписка активна</b>\n\n"
                f"📅 Осталось: <b>{max(1, days_left)} дн.</b>\n"
                f"📆 До: {user.subscription_until.strftime('%d.%m.%Y %H:%M')}\n\n"
                f"💡 Можешь продлить заранее - время добавится к остатку"
            )
        else:
            text = (
                "❌ <b>Подписка не активна</b>\n\n"
                "Оформи подписку, чтобы пользоваться трекером"
            )
        
        await message.answer(text, reply_markup=get_main_menu(
            has_access=user.is_admin or user.subscription_active
        ))


@dp.message(F.text == "❓ Как это работает")
async def how_it_works(message: Message):
    """Информация о работе трекера"""
    text = (
        "📖 <b>Как работает трекер</b>\n\n"
        "🔍 <b>Что делает:</b>\n"
        "• Ищет новые лоты Gift NFT\n"
        "• Отслеживает снижения цен\n"
        "• Показывает рейтинг и NFT продавца\n\n"
        "🎯 <b>Система занятости:</b>\n"
        "• Ты занимаешь продавца - он только твой\n"
        "• Никто другой его не получит\n"
        "• Можешь спокойно договариваться\n\n"
        "📊 <b>Разделы:</b>\n"
        "• Ширпы до 10 TON\n"
        "• Дорогие от 10 TON\n"
        "• Шрифты в имени\n"
        "• Черный фон\n"
        "• Нищуки (свой фильтр)\n"
        "• Свой раздел с любыми фильтрами\n\n"
        "💡 Просто выбери раздел и начни поиск!"
    )
    await message.answer(text)


@dp.message(F.text == "💬 Помощь с оплатой")
async def payment_help(message: Message):
    """Помощь с оплатой"""
    text = (
        "💬 <b>Нужна помощь с оплатой?</b>\n\n"
        "Напиши в поддержку, мы поможем разобраться"
    )
    
    if config.SUPPORT_USERNAME:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📱 Написать в поддержку",
                url=f"https://t.me/{config.SUPPORT_USERNAME.replace('@', '')}"
            )]
        ])
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(text)


# Подключаем обработчики оплаты
from bot.handlers.payment import router as payment_router
dp.include_router(payment_router)


async def main():
    """Запуск бота"""
    # Инициализируем базу данных
    await init_db()
    logger.info("Database initialized")
    
    # Запускаем бота
    logger.info("Starting bot...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
