from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import main_menu
from config import ABOUT_TEXT, CONTACT_TEXT, ADMIN_ID, WELCOME_TEXT

router = Router()

class FormStates(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_email = State()
    waiting_message = State()

@router.message(lambda msg: msg.text and msg.text.startswith('/start'))
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_menu())

@router.message(lambda msg: msg.text and msg.text.startswith('/help'))
async def cmd_help(message: Message):
    help_text = """
<b>📖 Справка</b>

/start - Главное меню
/help - Эта справка

Используйте кнопки внизу экрана 👇
"""
    await message.answer(help_text, reply_markup=main_menu())

@router.message(F.text == 'ℹ️ О компании')
async def show_about(message: Message):
    await message.answer(ABOUT_TEXT, reply_markup=main_menu())

@router.message(F.text == '📞 Контакты')
async def show_contacts(message: Message):
    await message.answer(CONTACT_TEXT, reply_markup=main_menu())

@router.message(F.text == '📝 Оставить заявку')
async def start_form(message: Message, state: FSMContext):
    await message.answer(
        "<b>📋 Форма заявки</b>\n\nУкажите ваше имя:"
    )
    await state.set_state(FormStates.waiting_name)

@router.message(FormStates.waiting_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Спасибо! Укажите номер телефона:")
    await state.set_state(FormStates.waiting_phone)

@router.message(FormStates.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Укажите ваш email (или напишите «нет»):")
    await state.set_state(FormStates.waiting_email)

@router.message(FormStates.waiting_email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Опишите, что вас интересует:")
    await state.set_state(FormStates.waiting_message)

@router.message(FormStates.waiting_message)
async def process_message(message: Message, state: FSMContext):
    data = await state.get_data()

    admin_text = f"""
<b>🆕 НОВАЯ ЗАЯВКА!</b>

<b>👤 Имя:</b> {data['name']}
<b>📱 Телефон:</b> {data['phone']}
<b>📧 Email:</b> {data['email']}
<b>💬 Интересует:</b> {message.text}

<b>👤 User ID:</b> {message.from_user.id}
<b>🕐 Время:</b> {message.date}
"""

    try:
        await message.bot.send_message(ADMIN_ID, admin_text)
        status = "✅ Заявка отправлена!"
    except Exception:
        status = "⚠️ Ошибка при отправке. Позвоните: +7 (4012) XXX-XX-XX"

    await message.answer(
        f"""<b>✅ Спасибо, {data['name']}!</b>

Ваша заявка принята.

📞 <b>Мы свяжемся с вами в ближайшее время!</b>

{status}""",
        reply_markup=main_menu()
    )

    await state.clear()

@router.message()
async def fallback(message: Message):
    await message.answer(
        "Используйте, пожалуйста, кнопки меню снизу 👇",
        reply_markup=main_menu()
    )
