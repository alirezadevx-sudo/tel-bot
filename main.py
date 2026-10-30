import requests
from sqlalchemy import select
import asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict 
from pydantic import SecretStr
from aiogram import Dispatcher, Bot
from aiogram import filters
from aiogram.types import Message
from db.models import User, Jokes
from schemas.schemas import RandJokeModel
from db.database import SessionLocal

class GeneralSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    
    token: SecretStr
    
settings = GeneralSettings()

async def get_joke() -> dict:
    url = "https://v2.jokeapi.dev/joke/Any?nsfw"

    res = requests.get(url, timeout=10)
    res.raise_for_status()

    data = res.json()

    if data.get("error"):
        raise RuntimeError("JokeAPI returned an error")

    return data

app = Dispatcher()

@app.message(filters.Command("help"))
async def help_(msg: Message):
    await msg.answer(
        text="👋 <b>Welcome to the Joke Bot!</b>\n\n"
        "Looking for a laugh? You're in the right place! 😂\n\n"
        "<b>📋 Available Commands</b>\n\n"
        "/start — Get started with the bot.\n"
        "/rand_joke — Get a random joke. 😄\n"
        "/help — Display this help message.\n\n"
        "<b>💡 How does it work?</b>\n\n"
        "Simply type /rand_joke and I'll fetch a joke for you. "
        "Enjoy the jokes, and remember to have fun! 🎭",
        parse_mode="HTML",
    )
    
@app.message(filters.CommandStart())
async def start(msg: Message):
    async with SessionLocal() as session:

        stmt = select(User).where(User.id == msg.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            await msg.answer(f"This user's info has already been saved in the database\nHere are the records:\n\nid: {user.id} | full name: {user.full_name} | date: {user.created_at}")
            return
            
        user_model = User(id=msg.from_user.id ,full_name=msg.from_user.full_name)
        session.add(user_model)
        await session.commit()
        await session.refresh(user_model)
        
        await msg.answer(f"Hello {msg.from_user.full_name}. You'r info has been documented in database.\nPlease use '\help' for more information.")

@app.message(filters.Command("rand_joke"))
async def rand_joke(msg: Message):
    try:
        data = await get_joke()



        if data["type"] == "single":
            joke_text = data["joke"]
        else:
            joke_text = f'{data["setup"]}  -  {data["delivery"]}'

        joke_data = RandJokeModel(
            joke_id=data["id"],
            joke_type=data["type"],
            joke=joke_text,
        )

        async with SessionLocal() as session:
            stmt = select(Jokes).where(Jokes.joke_id == data['id'])
            result = await session.execute(stmt)
            similar_joke = result.scalar_one_or_none()
            
            if similar_joke is not None:
                await msg.reply(joke_data.joke)
                return
            
            joke_db = Jokes(**joke_data.model_dump())

            session.add(joke_db)
            await session.commit()

        await msg.reply(joke_data.joke)

    except Exception:
        await msg.reply("Sorry, I couldn't fetch or save a joke.")
        raise
        
async def main():
    bot = Bot(token=settings.token.get_secret_value())
    await app.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())



