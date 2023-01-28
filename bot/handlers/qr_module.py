import os

import qrcode
import validators
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile

from bot_init import bot, cancel_kb


class QrState(StatesGroup):
    get_url = State()


# @dp.message_handler(commands=['qr'])
async def qr(message: types.Message, state: FSMContext):
    """
    Реагирует на команду /qr
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text="Пришли мне ссылку, для которой нужно сделать QR код =)", reply_markup=cancel_kb)
    await state.set_state(QrState.get_url.state)


# @dp.message_handler(state=QrState.get_url)
async def get_url_qr(message: types.Message, state: FSMContext):
    long_url = message.text.strip()

    if long_url == "skip":
        await bot.send_message(message.from_user.id, "Ок, отмена =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

    elif not validators.url(long_url):
        await message.reply("Кажется ссылка нерабочая попробуй снова =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

    else:
        img = qrcode.make(long_url)
        img.save("tmp.png")
        code_img = InputFile("tmp.png")
        await bot.send_photo(message.from_user.id, caption="Лови свой QR код! =)", photo=code_img, reply_markup=types.ReplyKeyboardRemove())
        os.remove("tmp.png")
        await state.finish()


def create_handlers_qr(dp: Dispatcher):
    dp.register_message_handler(qr, commands=['qr'], state="*")
    dp.register_message_handler(get_url_qr, state=QrState.get_url)
