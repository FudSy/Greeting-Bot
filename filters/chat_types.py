from config import admins
from aiogram.types import Message
from aiogram.filters import Filter

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in admins