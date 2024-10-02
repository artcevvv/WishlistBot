import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logger = logging.getLogger(__name__)

# Main bot variables

bot = Bot(token=TG_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) 
