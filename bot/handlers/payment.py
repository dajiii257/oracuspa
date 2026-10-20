# Обработчики оплаты через Telegram Stars

import logging
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, 
    PreCheckoutQuery, 
    Message,
    LabeledPrice,
)
from aiogram.filters import Command
from sqlalchemy import select, update

import config
from database import AsyncSessionLocal
from database.models import User, Payment
from bot.keyboards import get_main_menu

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data.startswith("buy_"))
async def process_tariff_selection(callback: CallbackQuery):
    """Обработка выбора тарифа"""
    tariff_code = callback.data.replace("buy_", "")
    tariff = config.TARIFFS.get(tariff_code)
    
    if not tariff:
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return
    
    async with AsyncSessionLocal() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
            return
        
        # Создаем платеж в базе
        payment = Payment(
            user_id=user.id,
            tariff_code=tariff_code,
            tariff_title=tariff["title"],
            payment_method="stars",
            amount=f"{tariff['price_stars']} ⭐",
            price_stars=tariff["price_stars"],
            status="pending"
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        
        # Создаем инвойс для Telegram Stars
        prices = [LabeledPrice(
            label=tariff["title"],
            amount=tariff["price_stars"]
        )]
        
        try:
            await callback.message.answer_invoice(
                title=f"Ocerao Tracker - {tariff['title']}",
                description=f"Подписка на трекер лотов Gift NFT",
                payload=f"payment_{payment.id}",
                provider_token="",  # Пустой для Stars
                currency="XTR",  # Telegram Stars
                prices=prices,
                max_tip_amount=0,
                suggested_tip_amounts=[],
            )
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            await callback.answer(
                "❌ Ошибка создания счета. Попробуйте позже",
                show_alert=True
            )


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    """Pre-checkout query для Stars"""
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """Обработка успешной оплаты Stars"""
    payment_info = message.successful_payment
    payload = payment_info.invoice_payload
    
    # Извлекаем ID платежа из payload
    if not payload.startswith("payment_"):
        logger.error(f"Invalid payload: {payload}")
        return
    
    try:
        payment_id = int(payload.replace("payment_", ""))
    except ValueError:
        logger.error(f"Invalid payment ID in payload: {payload}")
        return
    
    async with AsyncSessionLocal() as session:
        # Получаем платеж
        result = await session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        payment = result.scalar_one_or_none()
        
        if not payment:
            logger.error(f"Payment not found: {payment_id}")
            return
        
        # Обновляем статус платежа
        payment.status = "paid"
        payment.paid_at = datetime.utcnow()
        payment.telegram_payment_charge_id = payment_info.telegram_payment_charge_id
        
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.id == payment.user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.error(f"User not found: {payment.user_id}")
            return
        
        # Выдаем подписку
        tariff = config.TARIFFS.get(payment.tariff_code)
        if not tariff:
            logger.error(f"Tariff not found: {payment.tariff_code}")
            return
        
        if tariff["duration_seconds"] is None:
            # Навсегда
            user.subscription_forever = True
            user.subscription_active = True
            user.subscription_until = None
        else:
            # На определенный срок
            if user.subscription_active and user.subscription_until and user.subscription_until > datetime.utcnow():
                # Продление - добавляем к остатку
                user.subscription_until += timedelta(seconds=tariff["duration_seconds"])
            else:
                # Новая подписка
                user.subscription_until = datetime.utcnow() + timedelta(seconds=tariff["duration_seconds"])
            
            user.subscription_active = True
        
        await session.commit()
        
        # Обрабатываем реферала
        if user.referrer_id and config.REFERRAL_ENABLED:
            # Получаем реферера
            result = await session.execute(
                select(User).where(User.id == user.referrer_id)
            )
            referrer = result.scalar_one_or_none()
            
            if referrer:
                # Начисляем бонус
                referrer.referrals_paid += 1
                
                if referrer.subscription_active and referrer.subscription_until:
                    referrer.subscription_until += timedelta(seconds=config.REFERRAL_BONUS_SECONDS)
                elif not referrer.subscription_forever:
                    referrer.subscription_until = datetime.utcnow() + timedelta(seconds=config.REFERRAL_BONUS_SECONDS)
                    referrer.subscription_active = True
                
                await session.commit()
                
                # Уведомляем реферера
                try:
                    from bot.main import bot
                    bonus_hours = config.REFERRAL_BONUS_SECONDS // 3600
                    await bot.send_message(
                        referrer.id,
                        f"🎁 <b>Реферальный бонус!</b>\n\n"
                        f"Твой друг оформил подписку\n"
                        f"Тебе начислено: <b>+{bonus_hours} часов</b>"
                    )
                except Exception as e:
                    logger.error(f"Error sending referral notification: {e}")
        
        # Отправляем подтверждение
        if tariff["duration_seconds"] is None:
            sub_text = "Подписка навсегда активирована! 🎉"
        else:
            days = tariff["duration_seconds"] // 86400
            sub_text = f"Подписка на {days} дн. активирована! 🎉"
        
        await message.answer(
            f"✅ <b>Оплата прошла успешно!</b>\n\n"
            f"{sub_text}\n\n"
            f"Трекер открыт, можешь начинать работу 🚀",
            reply_markup=get_main_menu(has_access=True)
        )
        
        logger.info(f"Payment successful: user={user.id}, tariff={payment.tariff_code}, amount={payment.price_stars} stars")


@router.message(Command("promo"))
async def process_promo_code(message: Message):
    """Активация промокода"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "❌ Укажите промокод\n\n"
            "Использование: <code>/promo КОД</code>"
        )
        return
    
    promo_code = args[1].strip().upper()
    
    async with AsyncSessionLocal() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("❌ Ошибка: пользователь не найден")
            return
        
        # Ищем промокод в конфиге
        promo_data = config.PROMO_CODES.get(promo_code)
        
        if not promo_data:
            await message.answer("❌ Промокод не найден или уже не действует")
            return
        
        # Проверяем количество использований
        if "uses_left" in promo_data and promo_data["uses_left"] <= 0:
            await message.answer("❌ Промокод уже использован максимальное количество раз")
            return
        
        # Активируем промокод
        duration = promo_data.get("duration_seconds")
        
        if duration is None:
            # Навсегда
            user.subscription_forever = True
            user.subscription_active = True
            user.subscription_until = None
            bonus_text = "Подписка навсегда"
        else:
            # На определенный срок
            if user.subscription_active and user.subscription_until and user.subscription_until > datetime.utcnow():
                user.subscription_until += timedelta(seconds=duration)
            else:
                user.subscription_until = datetime.utcnow() + timedelta(seconds=duration)
            
            user.subscription_active = True
            days = duration // 86400
            hours = (duration % 86400) // 3600
            bonus_text = f"{days} дн." if days > 0 else f"{hours} ч."
        
        # Уменьшаем количество использований (в продакшене это должно быть в БД)
        if "uses_left" in promo_data:
            config.PROMO_CODES[promo_code]["uses_left"] -= 1
        
        await session.commit()
        
        await message.answer(
            f"✅ <b>Промокод активирован!</b>\n\n"
            f"🎁 Начислено: <b>{bonus_text}</b>\n\n"
            f"Трекер готов к работе 🚀",
            reply_markup=get_main_menu(has_access=True)
        )
        
        logger.info(f"Promo code activated: user={user.id}, code={promo_code}")
