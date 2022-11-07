from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create import bot
from users_db import new_user, get_admin_id, set_default


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Вас приветствует бот", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Встать в очередь", callback_data="start")))


async def command_start_(callback_query: types.CallbackQuery):
    await new_user(int(callback_query.from_user.id))
    await bot.send_message(callback_query.from_user.id, "Ожидайте пока с вами свяжется наш специалист")


async def send_code(callback_query: types.CallbackQuery):
    await bot.send_message(int(await get_admin_id(callback_query.message.chat.id)), "Пользователь отправил СМС на номер телефона",
                           reply_markup=InlineKeyboardMarkup()
                           .add(InlineKeyboardButton("Код пришел", callback_data="CodeTRUE"))
                           .add(InlineKeyboardButton("Код не пришел", callback_data=f"CodeFALSE{callback_query.message.chat.id}")))
    await bot.send_message(callback_query.message.chat.id, "Ожидайте от модератора СМС код")


async def false_code(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(int(callback_query.data.replace("CodeFALSE", "")), "Код не пришел, отправьте запрос еще раз",
                           reply_markup=InlineKeyboardMarkup()
                           .add(InlineKeyboardButton("Подтвердить ввод номера", callback_data="Подтвердить ввод номера")))


async def end_code(callback_query: types.CallbackQuery):
    admin_id = int(await get_admin_id(callback_query.message.chat.id))
    user_id = callback_query.message.chat.id
    await set_default(user_id, admin_id)
    await bot.send_message(user_id, "Операция завершена, чтобы вновь воспользоваться услугой нажмите кнопку", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Отправить запрос", callback_data="start")))
    await bot.send_message(admin_id, "Пользователь подтвердил корректность кода, чтобы подключиться к новому пользователю нажмите кнопку ниже", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Начать работу", callback_data="admin")))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_callback_query_handler(command_start_, lambda c: c.data == "start")
    dp.register_callback_query_handler(send_code, lambda c: c.data == "Подтвердить ввод номера")
    dp.register_callback_query_handler(end_code, lambda c: c.data == "Подтвердить код")
    dp.register_callback_query_handler(false_code, lambda c: c.data and c.data.startswith("CodeFALSE"), state="*")
