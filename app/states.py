from aiogram.fsm.state import State, StatesGroup


class UserRegister(StatesGroup):
    name = State()
    phone = State()


class AddTask(StatesGroup):
    task_title = State()


class FindTasks(StatesGroup):
    task_title = State()