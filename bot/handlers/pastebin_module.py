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


class PastebinState(StatesGroup):
    get_txt = State()
    short_url_pastebin = State()


async def pastebin(message: types.Message):
    """
    Реагирует на команду /pastebin
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text="Пришли мне текст на который нужно создать ссылку =)", reply_markup=cancel_kb)
    await PastebinState.get_txt.set()


async def get_txt(message: types.Message, state: FSMContext):
    pastebin_txt = message.text

    if pastebin_txt == 'cancel':
        await bot.send_message(message.from_user.id, text="Ок! Отмена =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await state.update_data(pastebin_txt=pastebin_txt)
        await message.answer("Отлично! A теперь отправь мне короткое название для ссылки или нажми кнопку skip, чтобы я сам сгенерировал название", reply_markup=skip_kb)
        await state.short_url_pastebin.set()


async def short_url_pastebin(message: types.Message, state: FSMContext):
    short_url = message.text.strip().lower()
    data = await state.get_data()
    collection = db['pastebin']
    if short_url == 'skip':
        short_url = compute_cheap_hash(data['pastebin_txt'])
        collection.insert_one(
            {"short_url": short_url, 'pastebin_txt': data['pastebin_txt']})
        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()
    else:
        tmp = collection.find_one({"short_url": short_url})
        if tmp is None:
            collection.insert_one(
                {"short_url": short_url, 'pastebin_txt': data['pastebin_txt']})
            await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"{MY_URL}{short_url}")
            await state.finish()
        else:
            await message.reply("Упс, кажется такое название уже занято, попробуй снова скоратить ссылку /shrink =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def create_handlers_pastebin(dp: Dispatcher):
    dp.register_message_handler(pastebin, commands=['pastebin'])
    dp.register_message_handler(get_txt, state=PastebinState.get_txt)
    dp.register_message_handler(
        short_url_pastebin, state=PastebinState.short_url_pastebin)
