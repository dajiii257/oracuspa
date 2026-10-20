# Клавиатуры для бота

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import config


def get_main_menu(has_access: bool = False) -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    
    if has_access:
        # Меню для пользователей с доступом
        keyboard = [
            [KeyboardButton(text="🚀 Открыть трекер")],
            [
                KeyboardButton(text="💎 Продлить"),
                KeyboardButton(text="📊 Моя подписка")
            ],
            [KeyboardButton(text="❓ Как это работает")]
        ]
    else:
        # Меню для пользователей без доступа
        keyboard = [
            [KeyboardButton(text="💎 Продлить")],
            [
                KeyboardButton(text="📊 Моя подписка"),
                KeyboardButton(text="❓ Как это работает")
            ],
            [KeyboardButton(text="💬 Помощь с оплатой")]
        ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
