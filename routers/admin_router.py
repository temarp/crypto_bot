import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.requests import add_user, get_text, get_all_text, edit_text, update_sub, get_users, get_referals
from keyboard.admin_kb import admin_start_kb, text_keyboard, admin_menu_kb, admin_kb_next, kb_users
from states import Admin




admin_router = Router()


@admin_router.callback_query(F.data == 'admin')
async def admin(callback: CallbackQuery):
    await callback.message.edit_text(text='Hello, Admin', reply_markup=admin_kb_next)


@admin_router.callback_query(F.data == 'admin_stat')
async def admin_stat(callback: CallbackQuery):
    users = await get_users()
    if len(users) == 0:
        await callback.message.edit_text(text='0 users', reply_markup=admin_menu_kb)

    users_kb = await kb_users(0)
    await callback.message.edit_text(text='Choose user', reply_markup=users_kb.as_markup())


@admin_router.callback_query(F.data == 'admin_text')
async def admin_text(callback: CallbackQuery):
    texts = list(await get_all_text())
    builder = await text_keyboard(texts)
    answ = ''
    for text in texts:
        answ += f'{text.id} - {text.name_text}\n'

    await callback.message.edit_text(text=f'Выбери текст, который хотите поменять\n\n{answ}', reply_markup=builder.as_markup())


@admin_router.callback_query(F.data == 'adm_back')
async def back(callback: CallbackQuery, state: FSMContext):
    text = await get_text(1)
    await callback.message.edit_text(text=text.text, reply_markup=admin_start_kb)
    await state.clear()


@admin_router.callback_query(F.data.startswith('text_'))
async def back(callback: CallbackQuery, state: FSMContext):
    id_ = int(callback.data.split('_')[-1])
    await state.set_state(Admin.id_text)
    await state.update_data(id_=id_)
    await callback.message.edit_text('Введите текст с форматированием, если оно нужно')


@admin_router.message(Admin.id_text)
async def edit_text_desc(message: Message, state: FSMContext):
    id_ = (await state.get_data())['id_']
    await edit_text(id_=id_, desc=message.html_text)
    await state.clear()
    await message.answer(text='Текст заменен!', reply_markup=admin_menu_kb)


@admin_router.callback_query(F.data.startswith('hash'))
async def activate_sub(callback: CallbackQuery, bot: Bot):
    text = await get_text(5)
    user_id = callback.data.split('_')[-1]
    price = callback.data.split('_')[1]
    await update_sub(user_id, price=price)
    await bot.send_message(chat_id=user_id, text=text.text)
    await callback.message.delete()


@admin_router.callback_query(F.data.startswith('user_'))
async def stat_user(callback: CallbackQuery):
    username = callback.data.split('_')[-1]

    kb = await kb_users(int(callback.data.split('_')[2]))

    id_ = callback.data.split('_')[1]

    ref = await get_referals(id_)
    date_now = datetime.date.today()

    list_current_week = list(filter(lambda x: 0 <= (date_now - x.date_sub).days < 7, ref))
    sub_current = len([i for i in list_current_week if i.price != 0])

    list_last_week = list(filter(lambda x: 7 <= (date_now - x.date_sub).days < 14, ref))
    sub_last = len([i for i in list_last_week if i.price != 0])

    sum_current_week = sum(i.price for i in list_current_week)
    sum_last_week = sum(i.price for i in list_last_week)

    total_sum = sum(i.price for i in ref)
    total_sub = len([i for i in ref if i.price != 0])
    text = (f'{username}\n\n<b>Current week</b>\n'
    f'Click: {len(list_current_week)}\n'
    f'Subscribers: {sub_current}\n'
    f'Profit: ${sum_current_week * 2}\n\n'

    f'<b>Last week</b>\n'
    f'Click: {len(list_last_week)}\n'
    f'Subscribers: {sub_last}\n'
    f'Profit: ${sum_last_week * 2}\n\n'

    '<b>Total</b>\n'
    f'Click: {len(ref)}\n'
    f'Subscribers: {total_sub}\n'
    f'Profit: ${total_sum * 2}')
    try:
        await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    except:
        pass


@admin_router.callback_query(F.data.startswith('page_'))
async def stat_user(callback: CallbackQuery):
    kb = await kb_users(int(callback.data.split('_')[-1]))

    await callback.message.edit_text(text='Choose user', reply_markup=kb.as_markup())