from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import admins
from keyboards import admin_keyboards

admin_router = Router()

@admin_router.message(Command("admin"))
async def get_admin_panel(message: Message, state: FSMContext):
    if message.from_user.id not in admins:
        await message.answer("У вас недостаточно прав!" + admins[0])
        return
    await state.clear()
    await message.answer("Выберите функцию", reply_markup=admin_keyboards.set_admin_keyboard())
