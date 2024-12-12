from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database import (get_user, get_tasks_by_user_id, get_task_ids_by_user_id_and_keywords)

from app.states import FindTasks


find = Router()


@find.callback_query(F.data.startswith("find_"))
async def find_tasks(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("Введите ключевое слово для поиска задачи",
                                  reply_markup=ikb.user_cancel)

    await state.set_state(FindTasks.task_title)


@find.message(FindTasks.task_title)
async def find_tasks_by_title(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(task_title=message.text)
        data = await state.get_data()

        task_title = data.get("task_title")
        user_id = message.from_user.id
        task_ids = await get_task_ids_by_user_id_and_keywords(user_id, task_title)

        if task_ids:
            await message.answer(f"Список задач по ключевому слову <u>{task_title}</u>:",
                                 parse_mode="HTML",
                                 reply_markup=await bkb.user_tasks_by_keywords(user_id, task_ids))
            await state.clear()
        else:
            await message.answer("Задачи не найдены!", reply_markup=ikb.user_cancel)
    else:
        await message.answer("Вы ничего не ввели!", reply_markup=ikb.user_cancel)



