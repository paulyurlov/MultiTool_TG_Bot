from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_init import MY_URL, bot, cancel_kb, compute_shurt_url, db, skip_kb


class PastebinState(StatesGroup):
    get_txt = State()
    short_url_pastebin = State()


async def pastebin(message: types.Message, state: FSMContext):
    """
    Реагирует на команду /pastebin
    :message: объект message
    """
    await bot.send_message(message.from_user.id, text="Пришли мне текст на который нужно создать ссылку =)", reply_markup=cancel_kb)
    await state.set_state(PastebinState.get_txt.state)


async def get_txt(message: types.Message, state: FSMContext):

    pastebin_txt = message.text

    if pastebin_txt == 'cancel':

        await bot.send_message(message.from_user.id, text="Ок! Отмена =)", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

    else:

        await state.update_data(pastebin_txt=pastebin_txt)
        await message.answer("Отлично! A теперь отправь мне короткое название для ссылки или нажми кнопку skip, чтобы я сам сгенерировал название", reply_markup=skip_kb)
        await state.set_state(PastebinState.short_url_pastebin.state)


async def short_url_pastebin(message: types.Message, state: FSMContext):

    short_url = message.text.strip().lower()
    data = await state.get_data()

    if short_url == 'skip':

        short_url = compute_shurt_url(data['pastebin_txt'])
        db['multi_tool'].insert_one(
            {"short_url": short_url, 'type': 'pastebin', 'pastebin_txt': data['pastebin_txt']})

        await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"{MY_URL}{short_url}")
        await state.finish()

    else:
        if db['multi_tool'].count_documents({"short_url": short_url}) == 0:

            db['multi_tool'].insert_one(
                {"short_url": short_url, 'type': 'pastebin', 'pastebin_txt': data['pastebin_txt']})

            await message.answer("Отлично! Лови короткую ссылку:", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"{MY_URL}{short_url}")
            await state.finish()

        else:

            await message.reply("Упс, кажется такое название уже занято, попробуй снова скоратить ссылку /shrink =)", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def create_handlers_pastebin(dp: Dispatcher):
    dp.register_message_handler(pastebin, commands=['pastebin'], state="*")
    dp.register_message_handler(get_txt, state=PastebinState.get_txt)
    dp.register_message_handler(
        short_url_pastebin, state=PastebinState.short_url_pastebin)
