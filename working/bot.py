import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# config logging
logging.basicConfig(level=logging.INFO)

# init bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start', 'help']))
async def command_start_handler(message):
    """
    This handler will be called when user sends `/start` or `/help` command 
    """
    await message.reply("Hi! I'm a chill guy bot!")

@dp.message()  # Changed from message_handler() to message()
async def echo(message: types.Message):
    """
    Echo message
    """
    await message.answer(message.text)

async def main():
    # Start polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())