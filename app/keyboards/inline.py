from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пройти регистрацию', callback_data='register')
        ]
    ]
)

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

user_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='cancel')
        ]
    ]
)

user_back_add_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить задачу', callback_data='add_new_task')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='cancel')
        ]
    ]
)