import validators
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_init import MY_URL, bot, cancel_kb, compute_shurt_url, db, skip_kb


class ShrinkState(StatesGroup):
    get_url = State()
    short_url = State()


# @dp.message_handler(commands=['shrink'])
async def shrink(message: types.Message, state: FSMContext):
    """
    Реагирует на команду /shrink
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text="Пришли мне ссылку, которую нужно уменьшить", reply_markup=cancel_kb)
    await state.set_state(ShrinkState.get_url.state)


# @dp.message_handler(state=ShrinkState.get_url)
async def get_url(message: types.Message, state: FSMContext):

    long_url = message.text.strip()
    if long_url == 'cancel':
        await bot.send_message(message.from_user.id, text="Ок! Отмена =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

    elif not validators.url(long_url):
        await message.reply("Кажется ссылка нерабочая попробуй снова =)")
        await state.finish()

    else:
        await state.update_data(long_url=long_url)
        await message.answer("Отлично! A теперь отправь мне короткое название для ссылки или нажми кнопку skip, чтобы я сам сгенерировал название", reply_markup=skip_kb)
        await state.set_state(ShrinkState.short_url.state)


# @dp.message_handler(state=ShrinkState.short_url)
async def short_url(message: types.Message, state: FSMContext):

    short_url = message.text.strip().lower()
    data = await state.get_data()

    if short_url == 'skip':

        short_url = compute_shurt_url(data['long_url'])
        db['multi_tool'].insert_one(
            {"short_url": short_url, 'type': 'link', 'original_url': data['long_url']})

        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()

    elif db['multi_tool'].count_documents({"short_url": short_url}) == 0:

        db['multi_tool'].insert_one(
            {"short_url": short_url, 'type': 'link', 'original_url': data['long_url']})

        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()

    else:
        await message.reply("Упс, кажется такое название уже занято, попробуй снова скоратить ссылку /shrink =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


def create_handlers_shrink(dp: Dispatcher):
    dp.register_message_handler(shrink, commands=['shrink'], state="*")
    dp.register_message_handler(get_url, state=ShrinkState.get_url)
    dp.register_message_handler(short_url, state=ShrinkState.short_url)
