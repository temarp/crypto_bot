from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='VIP', callback_data='payment'),
         InlineKeyboardButton(text='Results', url='https://t.me/crypto_pump_1000')],
        [InlineKeyboardButton(text='Partner Program', callback_data='ref')]
    ]
)

time_payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='1 Month: $250', callback_data='month_1')],
        [InlineKeyboardButton(text='6 Months: $450', callback_data='month_6')],
        [InlineKeyboardButton(text='Lifetime-VIP: $650', callback_data='month_100')],
        [InlineKeyboardButton(text='↩️', callback_data='cancel')]
    ]
)

payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='TRC-20', callback_data='trc'),
        InlineKeyboardButton(text='BEP-20', callback_data='bep')],
        [InlineKeyboardButton(text='↩️', callback_data='cancel')]
    ]
)

wallet_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Confirm Payment', callback_data='pay')],
        [InlineKeyboardButton(text='↩️', callback_data='cancel')]
    ]
)


back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='↩️', callback_data='cancel')]
    ]
)
