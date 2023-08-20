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
from bairbie import barbie

load_dotenv()

TOKEN = os.environ.get('BOT__TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


user_states = text.user_states
class UserState:
    def __init__(self):
        self.button_states = {
            'Bairbie': False,
            'Ken': False,
            'Blonde': False,
            'Brunette': False,
            'Red': False,
            'Black': False,
            'Tan': False,
            'Black ': False,
            'Light': False,
        }
        self.photo_path = None
        self.subscribed = False


# команда /start
@dp.message_handler(commands=[text.START_COMMAND])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = UserState()

    subscribed = await user_subscribed(user_id)
    if subscribed:
        with open("photo_for_the_team_start1.jpg", "rb") as photo: 
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Приветствую Вас! 🎀\n\nЯ - 🎀 Бот @barbiephotobot 🎀.\n\nПревращаю обычные фотографии в уникальный стиль Барби! 📸✨\\🌟 Отправьте вашу фотографию, и я превратю ее в нечто прекрасное! 🌟")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("Подписаться на Канал 1", url="https://t.me/thepriceofart"),
    

            # Добавьте остальные каналы аналогичным образом
            InlineKeyboardButton("Проверить подписку!", callback_data="after_subscription")
        )
        await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, подпишитесь на наши каналы, чтобы воспользоваться ботом.", reply_markup=keyboard)
#
def get_user_state(user_id):
    if user_id not in user_states:
        user_states[user_id] = UserState()
    return user_states[user_id]

async def toggle_button_state(user_id, button_id):
    user_state = get_user_state(user_id)
    user_state.button_states[button_id] = not user_state.button_states[button_id]

async def print_button_states(user_id):
    user_state = get_user_state(user_id)
    for button_id, is_checked in user_state.button_states.items():
        return

# Функция для создания клавиатуры
def create_keyboard(user_state):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Первый ряд из двух кнопок
    keyboard.row(
        types.InlineKeyboardButton(text='✅ Bairbie' if user_state.button_states['Bairbie'] else 'Bairbie', callback_data='Bairbie'),
        types.InlineKeyboardButton(text='✅ Ken' if user_state.button_states['Ken'] else 'Ken', callback_data='Ken')
    )
    
    # Второй ряд из одной статической кнопки
    keyboard.row(types.InlineKeyboardButton(text='Цвет волос:', callback_data='static_button1'))
    
    # Третий и четвертый ряды по две кнопки
    keyboard.row(
        types.InlineKeyboardButton(text='✅ Blonde' if user_state.button_states['Blonde'] else 'Blonde', callback_data='Blonde'),
        types.InlineKeyboardButton(text='✅ Brunette' if user_state.button_states['Brunette'] else 'Brunette', callback_data='Brunette')
    )
    keyboard.row(
        types.InlineKeyboardButton(text='✅ Red' if user_state.button_states['Red'] else 'Red', callback_data='Red'),
        types.InlineKeyboardButton(text='✅ Black' if user_state.button_states['Black'] else 'Black', callback_data='Black')
    )
    
    # Пятый ряд из одной статической кнопки
    keyboard.row(types.InlineKeyboardButton(text='Цвет кожи:', callback_data='static_button2'))
    
    # Шестой и седьмой ряды по две кнопки
    keyboard.row(
        types.InlineKeyboardButton(text='✅ Tan' if user_state.button_states['Tan'] else 'Tan', callback_data='Tan'),
        types.InlineKeyboardButton(text='✅ Light' if user_state.button_states['Light'] else 'Light', callback_data='Light'),
        types.InlineKeyboardButton(text='✅ Black' if user_state.button_states['Black '] else 'Black ', callback_data='Black ')
    )
    # восьмой ряд, для генерации фотографии
    keyboard.row(types.InlineKeyboardButton(text='Сгенерировать фотографию', callback_data='generate'))
    
    return keyboard

# Обработчик кнопки "Сгенерировать фотографию"
@dp.callback_query_handler(lambda c: c.data == 'generate')
async def process_generate_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_state = user_states.get(user_id)
    if user_state and user_state.photo_path:
        # Отправляем сообщение об ожидании
        with open("photo_2023-08-02_07-22-48.jpg", "rb") as processed_photo:
            await bot.send_photo(chat_id=user_id, photo=processed_photo, caption="🔄Ваша фотография в процессе преобразования. Пожалуйста, немного подождите...")
        inline_buttons1 = types.InlineKeyboardMarkup(row_width=1)
        topup_button1 = types.InlineKeyboardButton('Убрать водяной знак', callback_data="1")
        buy_vip_button1 = types.InlineKeyboardButton('купить VIP', callback_data="2")
        inline_buttons1.add(topup_button1, buy_vip_button1)
        selected_buttons = [button_id for button_id, is_checked in user_state.button_states.items() if is_checked]
        await barbie(selected_buttons[0], selected_buttons[1], selected_buttons[2], user_state.photo_path, user_id)
        with open(f"photos/{user_id}.jpg", "rb") as processed_photo:
            await bot.send_photo(chat_id=user_id, photo=processed_photo, caption="✨ Перевоплотись в стиль Барби и Кена!\n\n🎀Преобразуй обычные фото и делись ими с друзьями помощью нашего Бота @barbiephotobot", reply_markup=inline_buttons1)
    else:
        await bot.send_message(chat_id=user_id, text="⚠️ Пожалуйста, сначала отправьте фотографию.")

# Добавьте определение функции get_photo_path
async def get_photo_path(file_id):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)
    
    # Путь, куда вы сохраните фотографию на сервере
    local_path = f"photos/{file_id}.jpg"
    with open(local_path, 'wb') as f:
        f.write(downloaded_file.read())
    
    return local_path

@dp.callback_query_handler(lambda c: c.data in get_user_state(0).button_states.keys() or c.data.startswith("static_button"))
async def process_callback_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_state = get_user_state(user_id)
    button_id = callback_query.data
    
    if button_id.startswith("static_button"):
        return
    
    # Инвертируем состояние текущей кнопки
    await toggle_button_state(user_id, button_id)
    
    # Деактивируем кнопки в паре
    if button_id in ['Bairbie', 'Ken']:
        partner_button = 'Ken' if button_id == 'Bairbie' else 'Bairbie'
        user_state.button_states[partner_button] = False
    elif button_id in ['Blonde', 'Brunette', 'Red', 'Black']:
        partner_buttons = ['Blonde', 'Brunette', 'Red', 'Black']
        partner_buttons.remove(button_id)
        for partner_button in partner_buttons:
            user_state.button_states[partner_button] = False
    elif button_id in ['Tan', 'Light', 'Black ']:
        partner_buttons = ['Tan', 'Light', 'Black ']
        partner_buttons.remove(button_id)
        for partner_button in partner_buttons:
            user_state.button_states[partner_button] = False
    
    # Создаем новую клавиатуру с обновленными состояниями кнопок
    new_keyboard = create_keyboard(user_state)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=new_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'after_subscription')
async def process_after_subscription(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    subscribed = await user_subscribed(user_id)

    if subscribed:
        with open("photo_2023-08-02_07-22-03.jpg", "rb") as photo:
            await bot.send_photo(chat_id=user_id, photo=photo, caption="Приветствую Вас! 🎀\n\nЯ - 🎀 Бот @barbiephotobot 🎀.\n\nПревращаю обычные фотографии в уникальный стиль Барби! 📸✨\\🌟 Отправьте вашу фотографию, и я превратю ее в нечто прекрасное! 🌟", reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.answer_callback_query(callback_query.id, text="Пожалуйста, подпишитесь на наши каналы, чтобы воспользоваться ботом.", show_alert=True)

async def user_subscribed(user_id):
    user = await bot.get_chat_member(chat_id="@thepriceofart", user_id=user_id)
    return user.status == "member" or user.status == "administrator" or user.status == "creator"

@dp.message_handler(content_types=['photo'])
async def process_photo(message: types.Message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id)
    if user_state:
        subscribed = await user_subscribed(user_id)
        if subscribed:
            user_state.photo_path = await get_photo_path(message.photo[-1].file_id)
            with open("1_8164-fotor-2023082112849.jpg", "rb") as photo:
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="⚙️Создайте стильный образ, выбрав нужные опции:",  reply_markup=create_keyboard(user_state))
        else:
            await bot.send_message(chat_id=user_id, text="Для использования бота, пожалуйста, подпишитесь на наши каналы и нажмите /start снова.")
    else:
        await bot.send_message(chat_id=user_id, text="Чтобы начать, нажмите /start.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)