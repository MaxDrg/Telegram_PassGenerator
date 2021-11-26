import random
import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import state
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

vars = {}
number = '0123456789'
alpha = 'abcdefghijklmnopqrstuvwxyz'
alpha_up = alpha.upper()
character = '!@#$%^&*()_}{[]":;></?'

bot = Bot(token="2025840722:AAFMMuta_P4KHU4-qdjf1klsn-mF6IlHjMY")
dp = Dispatcher(bot, storage=MemoryStorage())

# Configure logging
logging.basicConfig(level=logging.INFO)

class States(state.StatesGroup):
    Length = state.State()

generate = KeyboardButton('Generate new password')
edit = KeyboardButton('Edit password length')

markup = ReplyKeyboardMarkup(resize_keyboard=True).row(generate, edit)

@dp.message_handler(commands="start")
async def Start(message: types.Message):
    mess = await message.reply("Create a unique password of any length\n\nDefault length - 8 characters", reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Generate new password')
async def gen_pass(message: types.Message):
    password = ""
    num = 8
    mess = await bot.send_message(message.from_user.id, "Your password has been generated!")
    for i in vars.keys():
        if i == message.from_user.id:
            num = int(vars.get(i))
    for i in range(0, num):
        num = random.choice(number)
        ch = random.choice(character)
        alp = random.choice(alpha)
        alp_up = random.choice(alpha_up)
        line = num + ch + alp + alp_up
        str = random.choice(line)
        password += str
    await message.reply(password, reply_markup=markup)


@dp.message_handler(lambda message: message.text == 'Edit password length')
async def edit_pass(message: types.Message):
    await message.reply("Enter new password length")
    await States.Length.set()

@dp.message_handler(state=States.Length)
async def edit_lingth(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(message.from_user.id, "You didn't enter an integer :(", reply_markup=markup)
        await state.finish()
        return
    elif int(message.text) <= 0:
        await bot.send_message(message.from_user.id, "You entered a wrong integer :(", reply_markup=markup)
        await state.finish()
        return
    elif int(message.text) >= 3900:
        await bot.send_message(message.from_user.id, "You entered too large a integer :(", reply_markup=markup)
        await state.finish()
        return
    global vars
    dict = {message.from_user.id: message.text}
    vars.update(dict)
    await bot.send_message(message.from_user.id, "Length changed :)", reply_markup=markup)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)