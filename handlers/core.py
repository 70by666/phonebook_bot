from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.core import kb_start
from service.settings import bot


async def start(message: types.Message):
    """
    Список команд и кнопки
    """
    await bot.send_message(
        message.chat.id, 
        'Выполнять команды только по форме ниже:\n'
        '/chatgpt [text]\n'
        '/addnumber - добавить новый номер\n'
        '/number - посмотреть номера по полю(Имя или Фамилия или Отчество)\n'
        '/getnumber - получить номер по ID',
        reply_markup=kb_start,
    )  


async def stop_fsm(message: types.Message, state: FSMContext):
    """
    Отмена машины состояний
    """
    current_state = await state.get_state()
    if current_state is None:
        return None
    
    await state.finish()
    await message.reply("ok", reply_markup=kb_start)  


async def delkb(message: types.Message):
    """
    Удаляет кнопки
    """
    kr = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'ok', reply_markup=kr)

    
def register_handlers_core(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(stop_fsm, state='*', commands="stop")
    dp.register_message_handler(delkb, commands=['убратькнопки'])
