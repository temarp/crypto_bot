import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboard.inline_kb import start_kb, payment_kb, wallet_kb, back_kb, time_payment_kb
from keyboard.admin_kb import admin_start_kb
from database.requests import get_text, add_user, update_sub, get_sub, get_referals, add_referal
from states import Payment
from config import ADMIN

main_router = Router()

@main_router.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    username = message.from_user.username
    if username is None:
        username = 'private'
    await add_user(tg_id=message.from_user.id, username=username)
    text = await get_text(1)
    await message.answer(text.text, reply_markup=start_kb)
    if message.from_user.id == int(command.args):
        return

    await add_referal(int(command.args), message.from_user.id)


@main_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN:

        username = message.from_user.username
        if username is None:
            username = 'private'

        await add_user(tg_id=message.from_user.id, username=username)
        text = await get_text(1)
        await message.answer(text.text, reply_markup=admin_start_kb)
        await state.clear()
        return

    await state.clear()
    username = message.from_user.username
    if username is None:
        username = 'private'
    await add_user(tg_id=message.from_user.id, username=username)
    text = await get_text(1)
    await message.answer(text.text, reply_markup=start_kb)


# @main_router.message()
# async def test(message: Message):
#     print(message.html_text)


@main_router.callback_query(F.data == 'payment')
async def time_pay(callback: CallbackQuery):
    await callback.message.edit_text(text='Choose a subscription period', reply_markup=time_payment_kb)


@main_router.callback_query(F.data.startswith('month'))
async def payment(callback: CallbackQuery, state: FSMContext):
    period = callback.data.split('_')[-1]
    if period == '1':
        period = '1 Month_250'
    elif period == '6':
        period = '6 Months_450'
    else:
        period = 'Lifetime-VIP_650'

    await state.set_state(Payment.period)
    await state.update_data(period=period)
    await callback.message.edit_text(text='Choose payment cryptocurrency:', reply_markup=payment_kb)


@main_router.callback_query(Payment.period, F.data == 'trc')
async def wallet(callback: CallbackQuery, state: FSMContext):
    text = await get_text(2)
    month = (await state.get_data())['period'].split('_')[0]
    text = text.text.format(month=month)
    await callback.message.edit_text(text=text, reply_markup=wallet_kb)




@main_router.callback_query(Payment.period, F.data == 'bep')
async def wallet(callback: CallbackQuery, state: FSMContext):
    text = await get_text(3)

    month = (await state.get_data())['period'].split('_')[0]
    text = text.text.format(month=month)
    await callback.message.edit_text(text=text, reply_markup=wallet_kb)


@main_router.callback_query(F.data == 'pay')
async def send_hash(callback: CallbackQuery, state: FSMContext):
    price = (await state.get_data())['period'].split('_')[-1]
    await state.set_state(Payment.hash_)
    await state.update_data(user_id=callback.from_user.id)
    await state.update_data(price=price)
    await callback.message.edit_text(text='Please send us a screenshot of the completed payment or the transaction hash.')


@main_router.message(Payment.hash_)
async def send_hash_to_admin(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Wait for confirmation', reply_markup=back_kb)
    data = await state.get_data()
    user_id = int(data['user_id'])
    price = int(data['price'])
    await state.clear()
    if message.photo:
        file_id = message.photo[-1].file_id
        hash_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Active', callback_data=f'hash_{price}_{user_id}')]
        ])
        await bot.send_photo(chat_id=ADMIN, reply_markup=hash_kb, photo=file_id)
        return

    hash_ = message.text
    hash_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Active', callback_data=f'hash_{price}_{user_id}')]
    ])
    await bot.send_message(chat_id=ADMIN, reply_markup=hash_kb, text=hash_)



@main_router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = await get_text(1)
    await callback.message.edit_text(text=text.text, reply_markup=start_kb)


@main_router.callback_query(F.data == 'ref')
async def check_ref(callback: CallbackQuery):
    ref = await get_referals(callback.from_user.id)
    date_now = datetime.date.today()

    list_current_week = list(filter(lambda x: 0 <= (date_now - x.date_sub).days < 7, ref))
    sub_current = len([i for i in list_current_week if i.price != 0])

    list_last_week = list(filter(lambda x: 7 <= (date_now - x.date_sub).days < 14, ref))
    sub_last = len([i for i in list_last_week if i.price != 0])

    sum_current_week = sum(i.price for i in list_current_week)
    sum_last_week = sum(i.price for i in list_last_week)

    total_sum = sum(i.price for i in ref)
    total_sub = len([i for i in ref if i.price != 0])

    text = await get_text(4)
    text = text.text.format(link='cryptopump1000_bot',
                            id=str(callback.from_user.id),
                            current_click=len(list_current_week),
                            current_subs=sub_current,
                            current_price=sum_current_week,
                            last_click=len(list_last_week),
                            last_subs=sub_last,
                            last_price=sum_last_week,
                            all_click=len(ref),
                            all_subs=total_sub,
                            all_price=total_sum)

    await callback.message.edit_text(text=text, reply_markup=back_kb)

