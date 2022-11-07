from aiogram import types
from aiogram.utils import executor

from create import dp
from handlers import client, admin
from users_db import sql_start


async def on_startup(dp):
    sql_start()
    await dp.bot.set_my_commands([types.BotCommand("start", "Запустить бота")])


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
