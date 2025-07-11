from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from middleware import jsonParser

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
    await state.clear()
    await message.answer(f'Вас зовут: {data["get_username"]}?\nВаше поздравление: {data["get_greeting"]}?')   