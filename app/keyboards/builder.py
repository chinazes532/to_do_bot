from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database import get_tasks_by_user_id, get_task, get_tasks_by_ids


async def user_panel(user_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Список задач", callback_data=f"list_{user_id}"))
    kb.row(InlineKeyboardButton(text="Найти задачу", callback_data=f"find_{user_id}"))
    kb.row(InlineKeyboardButton(text="Добавить задачу", callback_data="add_new_task"))

    return kb.as_markup()


async def user_tasks(user_id):
    kb = InlineKeyboardBuilder()

    tasks = await get_tasks_by_user_id(user_id)
    task = await get_task(tasks[0][0])
    for task in tasks:
        if task[3] == 0:
            kb.row(InlineKeyboardButton(text=f"{task[2]} 🚫", callback_data=f"task_{task[0]}"))
        else:
            kb.row(InlineKeyboardButton(text=f"{task[2]} ✅", callback_data=f"task_{task[0]}"))

    kb.row(InlineKeyboardButton(text="Назад", callback_data="cancel"))

    return kb.as_markup()


async def user_tasks_by_keywords(user_id, task_ids):
    kb = InlineKeyboardBuilder()

    # Получаем задачи по переданным идентификаторам
    tasks = await get_tasks_by_ids(task_ids)  # Предполагается, что эта функция реализована
    for task in tasks:
        if task[3] == 0:  # Предполагаем, что task[3] - это статус задачи
            kb.row(InlineKeyboardButton(text=f"{task[2]} 🚫", callback_data=f"task_{task[0]}"))
        else:
            kb.row(InlineKeyboardButton(text=f"{task[2]} ✅", callback_data=f"task_{task[0]}"))

    kb.row(InlineKeyboardButton(text="Назад", callback_data="cancel"))

    return kb.as_markup()



async def task_panel(task_id):
    kb = InlineKeyboardBuilder()
    task = await get_task(task_id)

    if task[3] == 0:
        kb.row(InlineKeyboardButton(text="✅ Задача выполнена", callback_data=f"done_{task_id}"))
        kb.row(InlineKeyboardButton(text="✅ Выполнить и удалить задачу", callback_data=f"delete_{task_id}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="cancel"))

    return kb.as_markup()