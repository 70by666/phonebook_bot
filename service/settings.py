import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData
from dotenv import find_dotenv, load_dotenv

# config

load_dotenv(find_dotenv())

storage = MemoryStorage()

bot = Bot(str(os.getenv('BOT_TOKEN')))

dp = Dispatcher(bot, storage=storage)

whitelist = str(os.getenv('WHITELIST')).split()

cd_edit = CallbackData('cd_edit', 'action', 'num_id')

cd_search = CallbackData('cd_search', 'action')
