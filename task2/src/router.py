from aiogram import Router, F
from aiogram.filters import Command, CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputFile, FSInputFile
from sqlalchemy import select

from database import async_session
from models import User
from states import MainState
from parser import scrape_category

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await message.answer('Привет! Я помогу получить тебе данные с сайта https://books.toscrape.com/')
    async with async_session() as session:
        stmt = select(User).filter_by(tg_id=message.from_user.id)
        user = await session.scalar(stmt)
        await state.set_state(MainState.url)
        if not user:
            await message.answer('Но для начала давай зарегистрируемся. Напиши свое имя.')
            await state.set_state(MainState.name)
        else:
            await message.answer('Укажи ссылку на категорию книг для получения данных.')


@router.message(MainState.name)
async def process_name(message: Message, state: FSMContext):
    async with async_session() as session:
        user = User(tg_id=message.from_user.id, name=message.text)
        session.add(user)
        await session.commit()

    await message.answer(f'Спасибо, {message.text}! Теперь укажи ссылку на категорию книг для получения данных.')
    await state.set_state(MainState.url)


@router.message(MainState.url)
async def process_url(message: Message, state: FSMContext):
    url = message.text
    if url.startswith('https://books.toscrape.com/catalogue/category/books/'):
        await message.answer(f'Кажется все в порядке, пробую получить данные')
        csv_file_path = await scrape_category(url)
        try:
            file = FSInputFile(csv_file_path)
            await message.answer("Данные успешно получены, отправляю файл...")
            await message.answer_document(file)
        except Exception:
            await message.answer('Похоже, что-то пошло не так. Давайте попробуем еще раз. Отправь корректную ссылку')
            await state.set_state(MainState.url)
            return
    else:
        await message.answer(f'Ссылка указана неверно. Попробуй еще раз.')
        await state.set_state(MainState.url)
        return
    await state.clear()


