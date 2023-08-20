import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio
from dotenv import load_dotenv
import os
import json

import text


load_dotenv()

TOKEN = os.environ.get('BOT__TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# команда /start
@dp.message_handler(commands=[text.START_COMMAND])
async def process_start_command(message: types.Message):
    
    with open("photo_for_the_team_start.jpg", "rb") as photo: 
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Приветствую Вас! 🎀\n\nЯ - 🎀 Бот @barbiephotobot 🎀.\n\nПревращаю обычные фотографии в уникальный стиль Барби! 📸✨\\🌟 Отправьте вашу фотографию, и я превратю ее в нечто прекрасное! 🌟")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)