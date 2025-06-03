from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Кредит"), KeyboardButton(text="Депозит")],
        [KeyboardButton(text="Ипотека"), KeyboardButton(text="Отпуск")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)