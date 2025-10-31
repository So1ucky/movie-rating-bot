import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import get_movies, get_data

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

start_message = '''Hi! This bot was created to search for movies, games, series and their data.

Usage:
Just type the title, for example, "Inception", "The Witcher"
Then select the desired one from the list of suggested ones'''

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(start_message)

@dp.message()
async def movie_handler(message: Message) -> None:
    data = get_movies(message.text)

    builder = InlineKeyboardBuilder()

    for i in data:
        builder.button(text=f'{i["Title"]}, {i["Type"]}', callback_data=str(i["IMDb"]))

    builder.adjust(1)
    markup = builder.as_markup()

    await message.answer("Choose the movie:", reply_markup=markup)

@dp.callback_query(F.data)
async def movie_callback(callback: CallbackQuery):
    movie = get_data(callback.data)

    if movie:
        text = f'🎬 {movie['Title']} ({movie["Year"]})\n📆 Release Date: {movie["Released"]}\n⏰ Runtime: {movie["Runtime"]}\n⭐ IMDb Rating: {movie["imdbRating"]}'
        await callback.message.answer_photo(photo=movie["Poster"].replace("SX300", "SX600"), caption=text)
        await callback.message.delete()
    else:
        await callback.message.edit_text("🤷‍♂️ Not found")

    await callback.answer()

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())