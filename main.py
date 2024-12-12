from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

class UserState (StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    print('привет! Я бот помогающий твоему здоровью.')
    await message.answer("привет! Я бот помогающий твоему здоровью.")

# возраст
@dp.message_handler(text= ["Calories"])
async def set_age(message):
    print("начало вычисления калорий")
    await message.answer("Введите свой возраст:")
    await UserState.age.set()
# рост
@dp.message_handler(state = UserState.age)
async def set_growth(message,state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

# вес
@dp.message_handler(state = UserState.growth)
async def set_weight(message,state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

# ответ калории
@dp.message_handler(state = UserState.weight)
async def send_calories(message,state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories1 = 10 * weight + 6.25 * growth - 5 * age + 5
    calories2 = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Ваша норма калорий {calories1} если вы мужчинка и {calories2} если вы женщинка")
    await state.finish()

@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
