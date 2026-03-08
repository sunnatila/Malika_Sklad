import asyncio
import logging
import sys

from loader import dp, bot, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup():
    await db.connect()
    logging.info("✅ PostgreSQL ga ulandi")

    await set_default_commands()
    await on_startup_notify()


async def on_shutdown():
    await db.disconnect()
    logging.info("🔴 PostgreSQL dan uzildi")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())