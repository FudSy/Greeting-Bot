from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import admins
from keyboards import admin_keyboards
from middleware import jsonParser
from handlers import start

admin_router = Router()

class Form(StatesGroup):
    phraseNumber = State()
    new_text = State()

@admin_router.message(Command("admin"), F.from_user.id.in_(admins))
async def get_admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите функцию", reply_markup=admin_keyboards.set_admin_keyboard())

@admin_router.message(F.text == "Настроить фразы")
async def configure_phrases(message: Message, state:FSMContext):
    await state.set_state(Form.phraseNumber)
    phrases = await jsonParser.load_phrases()
    await message.answer(text=f"Выберите какую фразу редактировать (1 или 2):\n\n1. {phrases['phrase_1']}\n2. {phrases['phrase_2']}", reply_markup=ReplyKeyboardRemove())

@admin_router.message(Form.phraseNumber, F.text.in_({"1", "2"}))
async def get_phrase_from_user(message: Message, state: FSMContext):
    await state.update_data(phraseNumber = message.text)
    await state.set_state(Form.new_text)
    await message.answer(text="Введите новый текст:")

@admin_router.message(Form.new_text, F.text)
async def update_phrase(message: Message, state: FSMContext):
    await state.update_data(new_text = message.text)
    data = await state.get_data()
    kb = [[InlineKeyboardButton(text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text=f"Ваш измененный текст:\n\n{data['new_text']}", reply_markup=keyboard)
    

@admin_router.callback_query(F.data == "yes")
async def write_phrase(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phrases = await jsonParser.load_phrases()
    phrases[f'phrase_{data["phraseNumber"]}'] = data["new_text"]
    await jsonParser.save_phrases(phrases)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Текст сохранен")
    await state.clear()
    await get_admin_panel(callback.message, state)

@admin_router.callback_query(F.data == "no")
async def write_phrase(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    await callback.answer("Текст отклонен")
    await state.clear()
    await get_admin_panel(callback.message, state)

@admin_router.message(F.text == 'Выйти из админ панели')
async def exit_admin_panel(message: Message, state: FSMContext):
    await message.answer(text='Выходим из админ панели')
    await start.cmd_start(message, state)