from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb


from app.database import get_user


stop = Router()


@stop.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user(user_id)

    if user:
        await callback.message.delete()
        await callback.message.answer(f"Привет, {callback.from_user.full_name}!\n"
                                      f"Выбери действие из меню ниже:",
                                      reply_markup=await bkb.user_panel(user_id))
    else:
        await callback.message.delete()
        await callback.answer("Регистрация отменена!")
        await callback.message.answer(f"Привет, {callback.from_user.full_name}!\n"
                             f"Для того, чтобы пользоваться ботом необходимо пройти регистрацию!",
                             reply_markup=ikb.register)
