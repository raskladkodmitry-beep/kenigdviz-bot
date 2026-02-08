from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📝 Оставить заявку')],
            [KeyboardButton(text='ℹ️ О компании')],
            [KeyboardButton(text='📞 Контакты')]
        ],
        resize_keyboard=True
    )
    return kb
