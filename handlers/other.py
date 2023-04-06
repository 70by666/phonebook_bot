from aiogram import Dispatcher, types

from keyboards.core import kb_start
from service.settings import bot


async def nocom(message: types.Message):
    await bot.send_message(message.chat.id, "Команда не существует", reply_markup=kb_start)
    await message.delete()


async def get_id(message: types.Message):
    """
    Команда чтобы получить id пользователя и чата
    """
    await bot.send_message(
        message.chat.id,
        f'chat: {message.chat.id}, user: {message.from_user.id}',
    )  


async def echo(message: types.Message):
    await bot.send_message(
        message.chat.id, 
        'Не понимаю о чем ты',
        reply_markup=kb_start,
    ) 
    await message.delete()
    
    
def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(get_id, commands=['id'])
    dp.register_message_handler(nocom, lambda message: message.text.startswith("/"))
    dp.register_message_handler(echo)
