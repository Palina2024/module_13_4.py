from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_messages(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Введи слово "calories", '
                         'чтобы узнать свою норму калорий в день для оптимального похудения или сохранения '
                         'нормального веса.')


@dp.message_handler(text='calories')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await message.answer('Введите свой рост:')
        await UserState.growth.set()
    else:
        await message.answer('Пожалуйста, введите корректное числовое значение возраста.')

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес:')
        await UserState.weight.set()
    else:
        await message.answer('Пожалуйста, введите корректное числовое значение для роста.')

@dp.message_handler(state=UserState.weight)
async def set_calories(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(weight=message.text)
        data = await state.get_data()
        age = int(data['age'])  # возраст
        growth = int(data['growth']) # рост
        weight = int(data['weight']) # вес
        # Пример формулы для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

        await message.answer(f'Для подсчета результата мы воспользовались формулой Миффлина-Сан Жеора. '
                             f'Ваша норма калорий: {calories} ккал.')
        await state.finish()
    else:
        await message.answer('Пожалуйста, введите корректное числовое значение для веса.')

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
