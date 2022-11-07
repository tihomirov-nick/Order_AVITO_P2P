from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=('5155157745:AAF9Apy-wTXdXoIewDYwoDfUMTpE_37ILvc'))
dp = Dispatcher(bot, storage=MemoryStorage())
