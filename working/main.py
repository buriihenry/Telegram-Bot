from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
import openai
import logging
import asyncio

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

class Reference:
    """
    This class is used to store previous reference from the OpenAI API.
    """
    def __init__(self) -> None:
        self.reference = ""

reference = Reference()

model_name = "gpt-3.5-turbo"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

def clear_past():
    """
    A handler to clear the past conversation and context.
    """
    reference.reference = ""

@router.message(Command(commands=['clear']))
async def clear(message: Message):
    """
    Clear the reference stored in the Reference class.
    """
    clear_past()
    await message.reply("Cleared the past convo!")

@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi! I'm a chill guy bot. Created by Burii. How can I assist you?")

@router.message(Command(commands=['help']))
async def helper(message: Message):
    """
    A helper function to provide assistance to the user.
    """
    help_message = """
    Hi! I'm a chill guy bot. I can help you generate text based on your input.
    /start - Start the bot
    /help - Get help
    /clear - Clear the reference
    I hope you have a great day!
    """
    await message.reply(help_message)

@router.message()
async def chatgpt(message: Message):
    """A handler to interact with the user and generate a response using the OpenAI API."""
    print(f">>>USER : {message.text}")
    try:
        openai.api_key = OPENAI_API_KEY
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set!")

        # Use the new API structure
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text},
            ]
        )

        # Extract the response content
        reply = response['choices'][0]['message']['content']
        reference.reference = reply  # Update reference
        print(f"<<<chatGPT : {reply}")
        await message.answer(reply)
    except Exception as e:
        logging.error(f"Error interacting with OpenAI API: {e}")
        await message.reply("Sorry, I encountered an error. Please try again later.")


async def main():
    # Include the router in the dispatcher
    dp.include_router(router)

    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)  # Ensures no updates are missed
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
