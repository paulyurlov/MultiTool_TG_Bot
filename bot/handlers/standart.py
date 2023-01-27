from aiogram import types, Dispatcher


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Реагирует на команду /start
    :message: объект message
    """
    await message.reply("Привет👋 \n\nЯ бот уменьшающий ссылки. Напиши /shrink чтобы начать =)")\


# @dp.message_handler(commands=['help'])
async def help(message: types.Message):
    """
    Реагирует на команду /start
    :message: объект message
    """
    await message.reply("Привет👋 \n\nЯ бот уменьшающий ссылки. Напиши /shrink чтобы начать =)")


def create_handlers_standart(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
