# Database Models для Ocerao Tracker

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Пользователь бота"""
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True)  # Telegram user ID
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    photo_url = Column(String(500), nullable=True)
    
    # Подписка
    is_admin = Column(Boolean, default=False)
    subscription_active = Column(Boolean, default=False)
    subscription_until = Column(DateTime, nullable=True)
    subscription_forever = Column(Boolean, default=False)
    trial_used = Column(Boolean, default=False)
    
    # Статистика
    lots_given = Column(Integer, default=0)
    lots_given_today = Column(Integer, default=0)
    lots_claimed = Column(Integer, default=0)
    lots_claimed_today = Column(Integer, default=0)
    last_reset_date = Column(DateTime, default=datetime.utcnow)
    
    # Реферальная система
    referrer_id = Column(BigInteger, nullable=True)
    referral_code = Column(String(50), unique=True, nullable=True)
    referrals_invited = Column(Integer, default=0)
    referrals_paid = Column(Integer, default=0)
    
    # Настройки пользователя (JSON)
    preferences = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    claimed_lots = relationship("ClaimedLot", back_populates="user")
    batches = relationship("Batch", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Lot(Base):
    """Лот Gift NFT"""
    __tablename__ = "lots"
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(String(100), unique=True, nullable=False)  # Уникальный ID лота
    
    # Информация о NFT
    title = Column(String(255), nullable=False)  # Plush Pepe #1234
    url = Column(String(500), nullable=False)  # t.me/nft/...
    collection = Column(String(255), nullable=True)
    
    # Изображения
    img_url = Column(String(500), nullable=True)
    img_alt_url = Column(String(500), nullable=True)
    
    # Цена
    currency = Column(String(10), nullable=False)  # "ton" или "stars"
    price = Column(Float, nullable=True)  # Цена в TON
    stars = Column(Integer, nullable=True)  # Цена в Stars
    old_price = Column(Float, nullable=True)  # Старая цена (если снижение)
    old_stars = Column(Integer, nullable=True)
    is_price_drop = Column(Boolean, default=False)
    
    # Атрибуты Gift NFT
    model = Column(JSON, nullable=True)  # {"name": "Model", "rarity": 5.2, "tier": "rare", "floor": 100}
    backdrop = Column(JSON, nullable=True)
    pattern = Column(JSON, nullable=True)
    
    # Продавец
    seller_id = Column(BigInteger, nullable=False)
    seller_username = Column(String(255), nullable=True)
    seller_name = Column(String(255), nullable=True)
    seller_avatar = Column(String(500), nullable=True)
    seller_premium = Column(Boolean, default=False)
    
    # Данные профиля продавца
    seller_level = Column(Integer, nullable=True)  # Рейтинг
    seller_nft_count = Column(Integer, nullable=True)  # Количество NFT
    seller_lots_count = Column(Integer, nullable=True)  # Лотов на продаже
    seller_dm_cost = Column(Integer, default=0)  # Стоимость ЛС в звездах
    
    # Фильтры продавца
    seller_is_girl = Column(Boolean, nullable=True)
    seller_is_anime = Column(Boolean, nullable=True)
    seller_is_fancy = Column(Boolean, nullable=True)  # Шрифт в имени
    seller_is_trader = Column(Boolean, nullable=True)  # Трейдер по имени
    seller_is_anon = Column(Boolean, nullable=True)  # Номер +888
    seller_one_username = Column(Boolean, nullable=True)
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_taken = Column(Boolean, default=False)  # Занят кем-то
    
    # Timestamps
    caught_at = Column(DateTime, default=datetime.utcnow)  # Когда поймали
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claimed_by = relationship("ClaimedLot", back_populates="lot")


class ClaimedLot(Base):
    """Занятый лот (связь пользователь-лот)"""
    __tablename__ = "claimed_lots"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    lot_id = Column(Integer, ForeignKey("lots.id"), nullable=False)
    
    claimed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="claimed_lots")
    lot = relationship("Lot", back_populates="claimed_by")


class Batch(Base):
    """Пачка лотов для пользователя"""
    __tablename__ = "batches"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    section_id = Column(Integer, nullable=False)  # ID раздела
    section_name = Column(String(255), nullable=False)
    want_count = Column(Integer, nullable=False)  # Сколько хотели
    found_count = Column(Integer, default=0)  # Сколько нашли
    
    is_done = Column(Boolean, default=False)
    note = Column(String(500), nullable=True)  # Сообщение в конце
    
    lot_ids = Column(JSON, default=[])  # Список ID лотов в пачке
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="batches")


class Section(Base):
    """Разделы трекера"""
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    hint = Column(String(500), nullable=True)
    icon = Column(String(50), default="spark")
    
    is_custom = Column(Boolean, default=False)  # Свой раздел пользователя
    is_rare = Column(Boolean, default=False)  # Редкий раздел
    
    # Фильтры раздела (JSON)
    filters = Column(JSON, default={})
    
    # Статистика
    ready_count = Column(Integer, default=0)  # Сколько готово сейчас
    rate = Column(Integer, default=0)  # Общее количество
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    """Платежи"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    # Тариф
    tariff_code = Column(String(50), nullable=False)  # "1day", "30days", "forever"
    tariff_title = Column(String(255), nullable=False)
    
    # Оплата
    payment_method = Column(String(50), nullable=False)  # "stars", "ton", "cryptobot"
    amount = Column(String(50), nullable=False)  # Сумма с валютой
    price_stars = Column(Integer, nullable=True)
    price_ton = Column(Float, nullable=True)
    
    # Telegram Stars Invoice
    invoice_payload = Column(String(255), nullable=True)
    telegram_payment_charge_id = Column(String(255), nullable=True)
    
    # Статус
    status = Column(String(50), default="pending")  # pending, paid, expired, cancelled
    
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="payments")


class PromoCode(Base):
    """Промокоды"""
    __tablename__ = "promo_codes"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    
    duration_seconds = Column(Integer, nullable=True)  # null = навсегда
    uses_total = Column(Integer, nullable=True)  # null = безлимит
    uses_left = Column(Integer, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class SellerCache(Base):
    """Кэш информации о продавцах"""
    __tablename__ = "seller_cache"
    
    seller_id = Column(BigInteger, primary_key=True)
    username = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    premium = Column(Boolean, default=False)
    
    level = Column(Integer, nullable=True)
    nft_count = Column(Integer, nullable=True)
    lots_count = Column(Integer, nullable=True)
    dm_cost = Column(Integer, default=0)
    
    is_girl = Column(Boolean, nullable=True)
    is_anime = Column(Boolean, nullable=True)
    is_fancy = Column(Boolean, nullable=True)
    is_trader = Column(Boolean, nullable=True)
    is_anon = Column(Boolean, nullable=True)
    one_username = Column(Boolean, nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
