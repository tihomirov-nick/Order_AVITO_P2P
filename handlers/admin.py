from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create import bot
from users_db import new_admin, check_for_free, start_dialog, get_user_id, get_admin_id, get_all_admins, get_all_users, set_default


async def admin_start(message: types.Message):
    await new_admin(int(message.from_user.id))
    if len((await check_for_free())) > 0:
        requests = InlineKeyboardMarkup()
        for i in range(len(await check_for_free())):
            requests.add(InlineKeyboardButton(text=f"Заявка от {(await check_for_free())[i][0]}", callback_data=f"connect{(await check_for_free())[i][0]}"))

        await bot.send_message(message.from_user.id, "Текущие заявки", reply_markup=requests)
    else:
        await bot.send_message(message.from_user.id, "Список заявок пуст",
                               reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton("Проверить заявки", callback_data="admin")))


async def admin_start_(callback_query: types.CallbackQuery):
    await new_admin(int(callback_query.from_user.id))
    if len((await check_for_free())) > 0:
        requests = InlineKeyboardMarkup()
        for i in range(len((await check_for_free()))):
            requests.add(InlineKeyboardButton(text=f"Заявка от {(await check_for_free())[i][0]}", callback_data=f"connect{(await check_for_free())[0][i]}"))
        await bot.send_message(callback_query.from_user.id, "Текущие заявки", reply_markup=requests)
    else:
        await bot.send_message(callback_query.from_user.id, "Список заявок пуст",
                               reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton("Проверить заявки", callback_data="admin")))


async def start_dial(callback_query: types.CallbackQuery):
    user_id = callback_query.data.replace('connect', '')
    admin_id = callback_query.from_user.id
    await start_dialog(user_id, admin_id)
    await bot.send_message(user_id, "Вы были подключены к специалисту, ожидайте его сообщение")
    await bot.send_message(admin_id, "Вы были подключены к пользователю, он ожидает ваше сообщение")


async def messenger(message: types.Message):
    if str(message.from_user.id) in str(await get_all_users()):
        await bot.send_message(int(await get_admin_id(message.from_user.id)), text=message.text, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Завершить заявку", callback_data=f"Завершить_заявку user {message.from_user.id}")))
    elif str(message.from_user.id) in str(await get_all_admins()):
        await bot.send_message(int(await get_user_id(message.from_user.id)), text=message.text, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Завершить заявку", callback_data=f"Завершить_заявку admin {message.from_user.id}")))


async def end_dial(callback_query: types.CallbackQuery):
    query = callback_query.data.replace("Завершить_заявку ", "")
    user_or_admin = query.split(" ")[0]
    user_or_admin_id = query.split(" ")[1]
    if user_or_admin == "admin":
        await bot.send_message(int(user_or_admin_id), text="Заявка завершена",
                               reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(text="Взять нового клиента", callback_data="admin")))
        await bot.send_message(int(await get_user_id(user_or_admin_id)), text="Заявка завершена",
                               reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(text="Встать в очередь", callback_data="start")))
        await set_default(user_or_admin_id, int(await get_user_id(user_or_admin_id)))
    elif user_or_admin == "user":
        await bot.send_message(int(user_or_admin_id), text="Заявка завершена",
                               reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(text="Встать в очередь", callback_data="start")))
        await bot.send_message(int(await get_admin_id(user_or_admin_id)), text="Заявка завершена",
                               reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(text="Взять нового клиента", callback_data="admin")))
        await set_default(user_or_admin_id, int(await get_admin_id(user_or_admin_id)))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['admin'])
    dp.register_callback_query_handler(admin_start_, lambda c: c.data == 'admin')
    dp.register_callback_query_handler(start_dial, lambda c: c.data and c.data.startswith('connect'))

    dp.register_message_handler(messenger, content_types=['text'])

    dp.register_callback_query_handler(end_dial, lambda c: c.data and c.data.startswith('Завершить_заявку '))
