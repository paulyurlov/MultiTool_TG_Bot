import validators
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from bot_init import bot, skip_kb, bot
from aiogram.types import InputFile
import qrcode


class QrState(StatesGroup):
    get_url = State()


# @dp.message_handler(commands=['qr'])
async def qr(message: types.Message):
    """
    Реагирует на команду /qr
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text="Пришли мне ссылку, для которой нужно сделать QR код =)", reply_markup=skip_kb)
    await QrState.get_url.set()


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
        await state.finish()


def create_handlers_qr(dp: Dispatcher):
    dp.register_message_handler(qr, commands=['qr'])
    dp.register_message_handler(get_url_qr, state=QrState.get_url)
