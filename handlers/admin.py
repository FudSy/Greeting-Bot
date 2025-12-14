from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import admins
from filters.chat_types import IsAdmin
from keyboards import admin_keyboards
from middleware import jsonParser
from handlers import start

admin_router = Router()

admin_router.message.filter(IsAdmin())

class Form(StatesGroup):
    phraseNumber = State()
    new_text = State()

    texts = {
        'Form:phraseNumber': 'Введите цифру снова:',
        'Form:new_text': 'Введите название заново:',
    }


@admin_router.message(Command("admin"), StateFilter("*"))
async def get_admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите функцию", reply_markup=admin_keyboards.set_admin_keyboard())

@admin_router.message(StateFilter(None), F.text == "Настроить фразы")
async def configure_phrases(message: Message, state:FSMContext):
    await state.set_state(Form.phraseNumber)
    phrases = await jsonParser.load_phrases()
    await message.answer(text=f"Выберите какую фразу редактировать (1 или 2):\n\n1. {phrases['phrase_1']}\n2. {phrases['phrase_2']}", reply_markup=ReplyKeyboardRemove())


@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=admin_keyboards.set_admin_keyboard())

@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == Form.phraseNumber:
        await message.answer('Предыдущего шага нет, или введите номер фразы для редактирования или напишите "отмена"')
        return

    previous = None
    for step in Form.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {Form.texts[previous.state]}")
            return
        previous = step


@admin_router.message(Form.phraseNumber, F.text.in_({"1", "2"}))
async def get_phrase_from_user(message: Message, state: FSMContext):
    await state.update_data(phraseNumber = message.text)
    await state.set_state(Form.new_text)
    await message.answer(text="Введите новый текст:")

@admin_router.message(Form.phraseNumber)
async def get_phrase_from_user(message: Message):
    await message.answer(text="Пожалуйста, введите 1 или 2, чтобы выбрать фразу для редактирования.")

@admin_router.message(Form.new_text, F.text)
async def update_phrase(message: Message, state: FSMContext):
    await state.update_data(new_text = message.text)
    data = await state.get_data()
    kb = [[InlineKeyboardButton(text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text=f"Ваш измененный текст:\n\n{data['new_text']}", reply_markup=keyboard)

@admin_router.message(Form.new_text, F.text)
async def update_phrase(message: Message):
    await message.answer(text="Пожалуйста, введите текст для обновления фразы.")

@admin_router.callback_query(F.data == "yes")
async def write_phrase(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phrases = await jsonParser.load_phrases()
    phrases[f'phrase_{data["phraseNumber"]}'] = data["new_text"]
    await jsonParser.save_phrases(phrases)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Текст сохранен")
    await state.clear()
    await callback.message.answer("Выберите функцию", reply_markup=admin_keyboards.set_admin_keyboard())

@admin_router.callback_query(F.data == "no")
async def write_phrase(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    await callback.answer("Текст отклонен")
    await state.clear()
    await callback.message.answer("Выберите функцию", reply_markup=admin_keyboards.set_admin_keyboard())

@admin_router.message(F.text == 'Выйти из админ панели')
async def exit_admin_panel(message: Message, state: FSMContext):
    await message.answer(text='Выходим из админ панели')
    await state.clear()
    phrases = await jsonParser.load_phrases()
    await message.answer(phrases['phrase_1'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(start.Form.get_username)