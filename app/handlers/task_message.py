from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database import (get_user, get_tasks_by_user_id,
                          insert_task, get_tasks_count_by_user_id_and_status,
                          get_task, update_task_status, delete_task)

from app.states import AddTask


task = Router()


@task.callback_query(F.data.startswith("list_"))
async def list_tasks(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    tasks = await get_tasks_by_user_id(user_id)
    count = await get_tasks_count_by_user_id_and_status(user_id, False)

    if tasks:
        await callback.message.delete()
        await callback.message.answer("Список Ваших задач:\n"
                                      f"Количество невыполненных задач: {count[0]}\n\n",
                                      reply_markup=await bkb.user_tasks(user_id))
    else:
        await callback.message.delete()
        await callback.message.answer("Список задач пуст!",
                                      reply_markup=ikb.user_back_add_task)


@task.callback_query(F.data == "add_new_task")
async def add_new_task(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("Введи задачу:",
                                  reply_markup=ikb.user_cancel)

    await state.set_state(AddTask.task_title)


@task.message(AddTask.task_title)
async def task_title(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(task_title=message.text)

        data = await state.get_data()
        task_title = data.get("task_title")
        user_id = message.from_user.id

        await insert_task(user_id, task_title, False)

        await message.answer("Задача была успешно добавлена!",
                             reply_markup=await bkb.user_panel(user_id))
    else:
        await message.answer("Текст задачи не может быть пустым!",
                             reply_markup=ikb.user_cancel)


@task.callback_query(F.data.startswith("task_"))
async def task_detail(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    task_id = int(callback.data.split("_")[1])
    task = await get_task(task_id)

    if task:
        await callback.message.answer(f"<b>Задача № {task[0]}</b>"
                                      f"\n\n<i>{task[2]}</i>\n\n"
                                      f"Статус задачи: {'<b>✅ Задача выполнена</b>' if task[3] else '<b>❌ Задача не выполнена</b>'}",
                                      parse_mode="HTML",
                                      reply_markup=await bkb.task_panel(task_id))
    else:
        await callback.message.answer("Задача не найдена!",
                                      reply_markup=ikb.user_back_add_task)


@task.callback_query(F.data.startswith("done_"))
async def done_task(callback: CallbackQuery):
    await callback.answer('Задача выполнена')
    await callback.message.delete()

    task_id = int(callback.data.split("_")[1])
    task = await get_task(task_id)

    await update_task_status(task_id, True)

    await callback.message.answer(f"<b>Задача № {task[0]}</b>"
                                  f"\n\n<i>{task[2]}</i>\n\n"
                                  f"Статус задачи: <b>✅ Задача выполнена</b>",
                                  parse_mode="HTML",
                                  reply_markup=await bkb.task_panel(task_id))


@task.callback_query(F.data.startswith("delete_"))
async def delete_task_handler(callback: CallbackQuery):
    await callback.answer('Задача выполнена')
    await callback.message.delete()

    task_id = int(callback.data.split("_")[1])
    await delete_task(task_id)

    await callback.message.answer("Задача была успешно выполнена и удалена!",
                                  reply_markup=await bkb.user_tasks(callback.from_user.id))




