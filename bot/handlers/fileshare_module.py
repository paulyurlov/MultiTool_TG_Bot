import io
import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_init import MY_URL, bot, cancel_kb, compute_shurt_url, db, fs, skip_kb


class FileShareState(StatesGroup):
    get_file = State()
    short_url = State()


async def file(message: types.Message, state: FSMContext):
    """
    Реагирует на команду /file
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text=f"Пришли мне файл на который нужно создать ссылку =)", reply_markup=cancel_kb)
    await state.set_state(FileShareState.get_file.state)


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
            await state.set_state(FileShareState.short_url.state)
        else:
            await bot.send_message(message.from_user.id, text="Опа, кажется ты не отправил файл, попробуй еще раз! =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


async def short_url_fileshare(message: types.Message, state: FSMContext):
    short_url = message.text.strip().lower()
    data = await state.get_data()
    if short_url == 'skip':
        short_url = compute_shurt_url(data['file_path'])
        file_id = None
        with io.FileIO(data['file_path'], 'r') as fileObject:
            file_id = fs.put(fileObject, filename=data['file_path'])
            print(file_id)

        os.remove(data['file_path'])

        db['multi_tool'].insert_one(
            {"short_url": short_url, 'type': 'file', 'file_id': file_id})
        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()
    else:
        if db['multi_tool'].count_documents({"short_url": short_url}) == 0:
            file_id = None
            with io.FileIO(data['file_path'], 'r') as fileObject:
                file_id = fs.put(fileObject, filename=data['file_path'])
                print(file_id)

            os.remove(data['file_path'])

            db['multi_tool'].insert_one(
                {"short_url": short_url, 'type': 'file', 'file_id': file_id})
            await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"{MY_URL}{short_url}")
            await state.finish()
        else:
            await message.reply("Упс, кажется такое название уже занято, попробуй снова скоратить ссылку /shrink =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def create_handlers_fileshare(dp: Dispatcher):
    dp.register_message_handler(file, commands="file", state="*")
    dp.register_message_handler(
        get_file, state=FileShareState.get_file, content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT])
    dp.register_message_handler(
        short_url_fileshare, state=FileShareState.short_url)
