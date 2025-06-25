import asyncio
from create_bot import bot, dp
from handlers import start, admin

async def main():
    dp.include_router(start.start_router)
    dp.include_router(admin.admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())