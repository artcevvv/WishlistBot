import logging

from aiogram.utils import executor

from components.cfg import *
from components.bot import *
from components.keyboards import *

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
