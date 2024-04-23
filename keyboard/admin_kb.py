from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_users


admin_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='VIP', callback_data='payment'),
         InlineKeyboardButton(text='Results', url='https://t.me/crypto_pump_1000')],
        [InlineKeyboardButton(text='Partner Program', callback_data='ref')],
        [InlineKeyboardButton(text='ADMIN', callback_data='admin')]
    ]
)


admin_kb_next = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Texts', callback_data='admin_text')],
        [InlineKeyboardButton(text='Statistics', callback_data='admin_stat')]
    ]
)

async def text_keyboard(texts: list):
    builder = InlineKeyboardBuilder()
    sp_buttons = []
    for key in texts:
        sp_buttons.append(InlineKeyboardButton(text=str(key.id), callback_data=f'text_{key.id}'))

    builder.row(*sp_buttons)
    builder.row(InlineKeyboardButton(text='Back', callback_data='adm_back'))
    return builder


admin_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Menu', callback_data='adm_back')]
    ]
)


async def kb_users(index):
    users = await get_users()
    users = [users[i:i + 10] for i in range(0, len(users), 10)]
    builder = InlineKeyboardBuilder()
    sp_buttons = []

    for user in users[index]:
        data = '@' + user.username if user.username != 'private' else str(user.user_id)
        sp_buttons.append(InlineKeyboardButton(text=data,
                                               callback_data=f'user_{user.user_id}_{index}_{data}'))
    builder.row(*sp_buttons, width=2)
    if index == 0 and len(users) == 1:
        builder.row(InlineKeyboardButton(text='Back', callback_data='adm_back'))
        return builder
    elif index == 0 and len(users) != 1:
        builder.row(InlineKeyboardButton(text='>>', callback_data=f'page_{index + 1}'))
        return builder

    elif index + 1 == len(users):
        builder.row(InlineKeyboardButton(text='<<', callback_data=f'page_{index - 1}'))
        return builder
    else:
        builder.row(InlineKeyboardButton(text='<<', callback_data=f'page_{index - 1}'),
                    InlineKeyboardButton(text='>>', callback_data=f'page_{index + 1}'), width=2)
        return builder


