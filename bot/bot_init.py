from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os
from pymongo import MongoClient, ASCENDING
import gridfs
import logging

load_dotenv()

# Get Bot token and MongoDB connection string from environment
API_TOKEN = os.environ['API_TOKEN']
CON_STRING = os.environ['CON_STRING']
MY_URL = os.environ['MY_URL']


# Init logger
bot_logger = logging.getLogger("bot")
bot_logger.setLevel(logging.INFO)
handler_logger = logging.FileHandler("bot.log", mode='w')
formatter_logger = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
handler_logger.setFormatter(formatter_logger)
bot_logger.addHandler(handler_logger)


# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# Initialize NoSQL DataBase
client = MongoClient(CON_STRING)
db = client['linkForwarder']
fs = gridfs.GridFS(db)

# _ = db['links'].drop_index('short_url')
_ = db['links'].create_index([('short_url', ASCENDING)],
                             unique=True)

# _ = db['pastebin'].drop_index('short_url')
_ = db['pastebin'].create_index([('short_url', ASCENDING)],
                                unique=True)

# Initialize skip Keyboard
button_skip = KeyboardButton('skip')
skip_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)
skip_kb.add(button_skip)

# Initialize cancel Keyboard
button_cancel = KeyboardButton('cancel')
cancel_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)
cancel_kb.add(button_cancel)
