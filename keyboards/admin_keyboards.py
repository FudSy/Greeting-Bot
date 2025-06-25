from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def set_admin_keyboard():
    kb = [
        [KeyboardButton(text="Настроить фразы")],
        [KeyboardButton(text="Поделиться номером")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    return keyboard