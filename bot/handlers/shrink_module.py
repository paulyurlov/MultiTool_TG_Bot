import validators
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
import hashlib
from bot_init import db, skip_kb, bot, cancel_kb, MY_URL


def compute_cheap_hash(txt, length=6):
    # This is just a hash for debugging purposes.
    #    It does not need to be unique, just fast and short.
    hash = hashlib.sha256(txt.encode('utf-8'))
    return hash.hexdigest()[:length]


class ShrinkState(StatesGroup):
    get_url = State()
    short_url = State()


# @dp.message_handler(commands=['shrink'])
async def shrink(message: types.Message):
    """
    Реагирует на команду /shrink
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text="Пришли мне ссылку, которую нужно уменьшить", reply_markup=cancel_kb)
    await ShrinkState.get_url.set()


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
        await state.short_url.set()


# @dp.message_handler(state=ShrinkState.short_url)
async def short_url(message: types.Message, state: FSMContext):
    short_url = message.text.strip().lower()
    data = await state.get_data()
    collection = db['links']
    if short_url == 'skip':
        short_url = compute_cheap_hash(data['long_url'])
        collection.insert_one(
            {"short_url": short_url, 'original_url': data['long_url']})
        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()
    else:
        tmp = collection.find_one({"short_url": short_url})
        if tmp is None:
            collection.insert_one(
                {"short_url": short_url, 'original_url': data['long_url']})
            await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"{MY_URL}{short_url}")
            await state.finish()
        else:
            await message.reply("Упс, кажется такое название уже занято, попробуй снова скоратить ссылку /shrink =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def create_handlers_shrink(dp: Dispatcher):
    dp.register_message_handler(shrink, commands=['shrink'])
    dp.register_message_handler(get_url, state=ShrinkState.get_url)
    dp.register_message_handler(short_url, state=ShrinkState.short_url)
