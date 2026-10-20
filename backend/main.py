# FastAPI Backend для MiniApp

import logging
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
from datetime import datetime
import json

import config
from database import AsyncSessionLocal, init_db
from database.models import User, Lot, Batch, ClaimedLot, Section, SellerCache
from backend.auth import verify_telegram_webapp_data
from backend.models import *
from utils.subscription_manager import check_and_grant_subscription

# Настройка логирования
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = FastAPI(title="Ocerao Tracker API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы фронтенда
app.mount("/tracker-app", StaticFiles(directory=config.FRONTEND_PATH + "/tracker-app", html=True), name="tracker-app")
app.mount("/js", StaticFiles(directory=config.FRONTEND_PATH + "/js"), name="js")
app.mount("/nft-img", StaticFiles(directory=config.FRONTEND_PATH + "/nft-img"), name="nft-img")
app.mount("/userpic", StaticFiles(directory=config.FRONTEND_PATH + "/userpic"), name="userpic")


# Dependency для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Dependency для аутентификации через Telegram WebApp
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из Telegram WebApp initData"""
    
    if not authorization or not authorization.startswith("tma "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    init_data = authorization.replace("tma ", "")
    
    # Верифицируем данные от Telegram
    user_data = verify_telegram_webapp_data(init_data)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Telegram data")
    
    # Получаем или создаем пользователя
    result = await db.execute(
        select(User).where(User.id == user_data["id"])
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Start the bot first")
    
    # Обновляем активность
    user.last_activity = datetime.utcnow()
    await db.commit()
    
    return user


# Dependency для проверки доступа
async def require_access(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Проверить наличие активной подписки"""
    has_access = await check_and_grant_subscription(db, user)
    
    if not has_access:
        raise HTTPException(status_code=402, detail="Subscription required")
    
    return user


@app.on_event("startup")
async def startup():
    """Инициализация при старте"""
    await init_db()
    logger.info("Backend API started")


# ============ ENDPOINTS ============

@app.get("/api/me")
async def get_me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о текущем пользователе"""
    
    # Проверяем доступ
    has_access = await check_and_grant_subscription(db, user)
    
    # Получаем разделы
    result = await db.execute(
        select(Section).where(Section.is_active == True)
    )
    sections = result.scalars().all()
    
    sections_data = []
    for section in sections:
        sections_data.append({
            "id": section.id,
            "name": section.name,
            "hint": section.hint,
            "icon": section.icon,
            "custom": section.is_custom,
            "set": bool(section.filters) if section.is_custom else True,
            "rare": section.is_rare,
            "rate": section.rate,
            "ready": section.ready_count
        })
    
    return {
        "user": {
            "id": user.id,
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username or "",
            "photo_url": user.photo_url or ""
        },
        "admin": user.is_admin,
        "access": has_access,
        "beta": user.is_admin,  # Пока только для админов
        "prefs": user.preferences or {},
        "sections": sections_data,
        "batch_max": config.MAX_BATCH_SIZE
    }


@app.get("/api/prefs")
async def get_prefs(user: User = Depends(require_access)):
    """Получить настройки пользователя"""
    return {"prefs": user.preferences or {}}


@app.post("/api/prefs")
async def update_prefs(
    data: dict,
    user: User = Depends(require_access),
    db: AsyncSession = Depends(get_db)
):
    """Обновить настройки пользователя"""
    
    # Обновляем настройки
    current_prefs = user.preferences or {}
    current_prefs.update(data)
    user.preferences = current_prefs
    
    await db.commit()
    
    return {"prefs": user.preferences}


@app.get("/api/profile")
async def get_profile(
    user: User = Depends(require_access),
    db: AsyncSession = Depends(get_db)
):
    """Получить профиль пользователя"""
    
    # Получаем занятые лоты
    result = await db.execute(
        select(ClaimedLot, Lot)
        .join(Lot, ClaimedLot.lot_id == Lot.id)
        .where(ClaimedLot.user_id == user.id)
        .order_by(ClaimedLot.claimed_at.desc())
        .limit(50)
    )
    claimed_lots = result.all()
    
    claimed_data = []
    for claimed, lot in claimed_lots:
        claimed_data.append({
            "listing": lot.listing_id,
            "title": lot.title,
            "url": lot.url,
            "img": lot.img_url,
            "img_alt": lot.img_alt_url,
            "currency": lot.currency,
            "price": lot.price,
            "stars": lot.stars,
            "seller": {
                "id": lot.seller_id,
                "username": lot.seller_username,
                "name": lot.seller_name,
                "avatar": lot.seller_avatar,
                "premium": lot.seller_premium
            },
            "claimed_at": int(claimed.claimed_at.timestamp())
        })
    
    # Статус подписки
    sub_data = {
        "admin": user.is_admin,
        "active": user.subscription_active,
        "forever": user.subscription_forever,
        "left": None
    }
    
    if user.subscription_until and not user.subscription_forever:
        left_seconds = int((user.subscription_until - datetime.utcnow()).total_seconds())
        sub_data["left"] = max(0, left_seconds)
    
    # Реферальная ссылка
    ref_link = f"https://t.me/{config.BOT_TOKEN.split(':')[0]}?start=ref_{user.id}"
    
    return {
        "stats": {
            "given": user.lots_given,
            "given_today": user.lots_given_today,
            "claimed": user.lots_claimed,
            "claimed_today": user.lots_claimed_today
        },
        "claimed": claimed_data,
        "sub": sub_data,
        "ref": {
            "link": ref_link,
            "bonus": "6 часов" if config.REFERRAL_ENABLED else None,
            "invited": user.referrals_invited,
            "paid": user.referrals_paid,
            "got": f"{user.referrals_paid * 6} ч" if config.REFERRAL_ENABLED else "0"
        }
    }


@app.get("/api/catalog")
async def get_catalog(user: User = Depends(require_access)):
    """Получить каталог коллекций, моделей, фонов и узоров"""
    
    # Здесь должны быть реальные данные из парсеров
    # Пока возвращаем данные из старого API как пример
    
    return {
        "collections": [
            "Plush Pepe", "Candy Cane", "Moon Pendant", "Star Notepad",
            # ... добавить больше из catalog.html
        ],
        "models": [
            "Classic", "Gold", "Silver", "Rainbow",
            # ... добавить больше
        ],
        "backdrops": [
            "Black", "Onyx Black", "Platinum", "Pure Gold",
            # ... добавить больше
        ],
        "patterns": [
            "Star", "Moon", "Sun", "Crown",
            # ... добавить больше
        ]
    }


@app.post("/api/batch")
async def create_batch(
    data: BatchCreateRequest,
    user: User = Depends(require_access),
    db: AsyncSession = Depends(get_db)
):
    """Создать новую пачку лотов"""
    
    section_id = data.section
    count = min(data.count, config.MAX_BATCH_SIZE)
    
    # Получаем раздел
    result = await db.execute(
        select(Section).where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Создаем пачку
    batch = Batch(
        user_id=user.id,
        section_id=section.id,
        section_name=section.name,
        want_count=count,
        found_count=0,
        is_done=False,
        lot_ids=[]
    )
    db.add(batch)
    await db.commit()
    await db.refresh(batch)
    
    # TODO: Запустить поиск лотов в фоне
    
    return {
        "batch": {
            "id": batch.id,
            "section": section.id,
            "section_name": section.name,
            "want": count,
            "done": False,
            "note": None,
            "cards": []
        }
    }


@app.get("/api/batch")
async def get_batch(
    user: User = Depends(require_access),
    db: AsyncSession = Depends(get_db)
):
    """Получить текущую пачку пользователя"""
    
    # Получаем последнюю активную пачку
    result = await db.execute(
        select(Batch)
        .where(Batch.user_id == user.id)
        .order_by(Batch.created_at.desc())
        .limit(1)
    )
    batch = result.scalar_one_or_none()
    
    if not batch:
        return {"batch": None}
    
    # Получаем лоты из пачки
    if batch.lot_ids:
        result = await db.execute(
            select(Lot).where(Lot.id.in_(batch.lot_ids))
        )
        lots = result.scalars().all()
    else:
        lots = []
    
    # Формируем данные карточек
    cards = []
    for lot in lots:
        # Проверяем, занят ли лот этим пользователем
        result = await db.execute(
            select(ClaimedLot).where(
                ClaimedLot.lot_id == lot.id,
                ClaimedLot.user_id == user.id
            )
        )
        claimed = result.scalar_one_or_none()
        
        cards.append({
            "listing": lot.listing_id,
            "title": lot.title,
            "url": lot.url,
            "img": lot.img_url,
            "img_alt": lot.img_alt_url,
            "currency": lot.currency,
            "price": lot.price,
            "stars": lot.stars,
            "old_price": lot.old_price,
            "old_stars": lot.old_stars,
            "drop": lot.is_price_drop,
            "model": lot.model,
            "backdrop": lot.backdrop,
            "pattern": lot.pattern,
            "seller": {
                "id": lot.seller_id,
                "username": lot.seller_username,
                "name": lot.seller_name,
                "avatar": lot.seller_avatar,
                "premium": lot.seller_premium,
                "level": lot.seller_level,
                "nft": lot.seller_nft_count,
                "paid": lot.seller_dm_cost,
                "loading": False
            },
            "caught": int(lot.caught_at.timestamp()),
            "claimed": bool(claimed),
            "taken": lot.is_taken
        })
    
    return {
        "batch": {
            "id": batch.id,
            "section": batch.section_id,
            "section_name": batch.section_name,
            "want": batch.want_count,
            "done": batch.is_done,
            "note": batch.note,
            "cards": cards
        }
    }


@app.post("/api/claim")
async def claim_lot(
    data: ClaimRequest,
    user: User = Depends(require_access),
    db: AsyncSession = Depends(get_db)
):
    """Занять лот"""
    
    # Получаем лот
    result = await db.execute(
        select(Lot).where(Lot.listing_id == data.listing)
    )
    lot = result.scalar_one_or_none()
    
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    
    # Проверяем, не занят ли уже
    if lot.is_taken:
        return {"ok": False, "message": "Этого продавца уже занял другой пользователь"}
    
    # Проверяем, не занимал ли уже этот пользователь
    result = await db.execute(
        select(ClaimedLot).where(
            ClaimedLot.lot_id == lot.id,
            ClaimedLot.user_id == user.id
        )
    )
    already_claimed = result.scalar_one_or_none()
    
    if already_claimed:
        return {"ok": True, "message": "Ты уже занял этого продавца"}
    
    # Занимаем лот
    claimed = ClaimedLot(
        user_id=user.id,
        lot_id=lot.id
    )
    db.add(claimed)
    
    lot.is_taken = True
    
    # Обновляем статистику
    user.lots_claimed += 1
    user.lots_claimed_today += 1
    
    await db.commit()
    
    # Получаем обновленную пачку
    result = await db.execute(
        select(Batch)
        .where(Batch.user_id == user.id)
        .order_by(Batch.created_at.desc())
        .limit(1)
    )
    batch = result.scalar_one_or_none()
    
    batch_data = None
    if batch:
        # TODO: вернуть полные данные пачки
        batch_data = {"id": batch.id}
    
    return {
        "ok": True,
        "batch": batch_data
    }


@app.post("/api/log")
async def log_event(
    data: dict,
    user: User = Depends(require_access)
):
    """Логирование событий (например, написать продавцу)"""
    logger.info(f"User event: user={user.id}, event={data.get('e')}, data={data}")
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
