from aiogram import executor
from bot_init import dp, bot_logger
from handlers import shrink_module, standart, qr_module, pastebin_module, fileshare_module


# Init command handlers

# Standart handlers /start and /help
standart.create_handlers_standart(dp)
bot_logger.info('Created standart commands handlers')

# Shrink handlers /shrink
shrink_module.create_handlers_shrink(dp)
bot_logger.info('Created /shrink command handlers')

# QR code handlers /qr
qr_module.create_handlers_qr(dp)
bot_logger.info('Created /qr command handlers')

# PasteBin handlers /pastebin
pastebin_module.create_handlers_pastebin(dp)
bot_logger.info('Created /pastebin command handlers')

# FileShare handlers /file
fileshare_module.create_handlers_fileshare(dp)
bot_logger.info('Created /file command handlers')


if __name__ == '__main__':
    bot_logger.info('Starting bot polling')
    executor.start_polling(dp, skip_updates=True)
