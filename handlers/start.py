from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from middleware import jsonParser
import db.queries

start_router = Router()

class Form(StatesGroup):
    get_username = State()
    get_greeting = State()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    phrases = await jsonParser.load_phrases()
    await message.answer(phrases['phrase_1'])
    await state.set_state(Form.get_username)

@start_router.message(Form.get_username, F.text)
async def getGreeting(message: Message, state: FSMContext):
    await state.update_data(get_username = message.text)
    await state.set_state(Form.get_greeting)
    phrases = await jsonParser.load_phrases()
    await message.answer(phrases['phrase_2'])

@start_router.message(Form.get_greeting, F.text)
async def summary(message: Message, state: FSMContext):
    await state.update_data(get_greeting = message.text)
    data = await state.get_data()
    kb = [[InlineKeyboardButton(text="Да", callback_data="yes_1"), InlineKeyboardButton(text="Нет", callback_data="no_1")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(f'Вас зовут: {data["get_username"]}?\nВаше поздравление: {data["get_greeting"]}?', reply_markup=keyboard)

@start_router.callback_query(F.data == "yes_1")
async def write_in_db(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.queries.insert_user(callback.from_user.id, data["get_username"], data["get_greeting"])
    await state.clear()

@start_router.callback_query(F.data == "no_1")
async def write_in_db(callback: CallbackQuery, state: FSMContext):
    await state.clear()    
    await cmd_start(callback.message, state)