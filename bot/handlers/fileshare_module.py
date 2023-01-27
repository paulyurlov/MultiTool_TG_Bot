from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
import hashlib
import io
from bot_init import fs, skip_kb, bot, cancel_kb, MY_URL
import os


# TODO Replace function on more reliable
def compute_cheap_hash(txt, length=6):
    # This is just a hash for debugging purposes.
    #    It does not need to be unique, just fast and short.
    hash = hashlib.sha256(txt.encode('utf-8'))
    return hash.hexdigest()[:length]


class FileShareState(StatesGroup):
    get_file = State()
    short_url = State()


async def file(message: types.Message):
    """
    Реагирует на команду /file
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text=f"Пришли мне файл на который нужно создать ссылку =)", reply_markup=cancel_kb)
    await FileShareState.get_file.set()


async def get_file(message: types.Message, state: FSMContext):
    txt = message.text.strip().lower()
    if txt == 'cancel':
        await bot.send_message(message.from_user.id, text="Ок! Отмена =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        tmp = message.document
        if tmp is not None:
            file_name = message.document.file_name
            await message.document.download(file_name)
            await state.update_data(file_path=file_name)
            await bot.send_message(message.from_user.id, text=f"Отлично! A теперь отправь мне короткое название для ссылки или нажми кнопку skip, чтобы я сам сгенерировал название", reply_markup=skip_kb)
            await FileShareState.short_url.set()
        else:
            await bot.send_message(message.from_user.id, text="Опа, кажется ты не отправил файл, попробуй еще раз! =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


async def short_url_fileshare(message: types.Message, state: FSMContext):
    short_url = message.text.strip().lower()
    data = await state.get_data()
    if short_url == 'skip':
        short_url = compute_cheap_hash(data['file_path'])
        with io.FileIO(data['file_path'], 'r') as fileObject:
            _ = fs.put(fileObject, filename=short_url)
        os.remove(data['file_path'])
        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()
    else:
        tmp = fs.find_one({"filename": short_url})
        if tmp is None:
            with io.FileIO(data['file_path'], 'r') as fileObject:
                _ = fs.put(fileObject, filename=short_url)
            os.remove(data['file_path'])
            await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"{MY_URL}{short_url}")
            await state.finish()
        else:
            await message.reply("Упс, кажется такое название уже занято, попробуй снова скоратить ссылку /shrink =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def create_handlers_fileshare(dp: Dispatcher):
    dp.register_message_handler(file, commands="file")
    dp.register_message_handler(
        get_file, state=FileShareState.get_file, content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT])
    dp.register_message_handler(
        short_url_fileshare, state=FileShareState.short_url)
