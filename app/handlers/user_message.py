from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb


from app.database import insert_user, get_user

from app.states import UserRegister

user = Router()


@user.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)

    if user:
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"Выбери действие из меню ниже:",
                             reply_markup=await bkb.user_panel(user_id))
    else:
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"Для того, чтобы пользоваться ботом необходимо пройти регистрацию!",
                             reply_markup=ikb.register)


@user.callback_query(F.data == 'register')
async def register(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("Для регистрации введи свое имя:",
                                  reply_markup=ikb.user_cancel)

    await state.set_state(UserRegister.name)


@user.message(UserRegister.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Теперь введи свой номер телефона в формате +79999999999:",
                         reply_markup=ikb.user_cancel)

    await state.set_state(UserRegister.phone)


@user.message(UserRegister.phone)
async def phone(message: Message, state: FSMContext):
    if len(message.text) == 12 and message.text[0] == "+" and message.text[1:].isdigit() and message.text[1] == "7" and message.text[2] == "9":
        await state.update_data(phone=message.text)

        data = await state.get_data()
        name = data.get("name")
        phone = data.get("phone")
        user_id = message.from_user.id
        username = message.from_user.username

        await insert_user(user_id, username, name, phone)

        await message.answer("Номер телефона успешно сохранен.\n"
                             "Теперь вам доступен полный функционал бота!",
                             reply_markup=await bkb.user_panel(user_id))
    else:
        await message.reply("Пожалуйста, введите номер телефона в формате +79999999999.",
                             reply_markup=ikb.user_cancel)