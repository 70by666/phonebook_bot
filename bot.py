from aiogram import executor

from handlers import add_number, core, edit_number, other, search_number
from service.settings import dp

core.register_handlers_core(dp)
search_number.register_handlers_search_number(dp)
add_number.register_handlers_add_number(dp)
edit_number.register_handlers_edit_number(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
