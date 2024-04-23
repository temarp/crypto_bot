from database.models import User, TextDesc, Referal, async_session

from sqlalchemy import Select, Delete, Update

async def add_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(Select(User).where(User.user_id == tg_id))

        if not user:
            session.add(User(user_id=tg_id, username=username))
            await session.commit()

async def get_sub(tg_id):
    async with async_session() as session:
        user = await session.scalar(Select(User).where(User.user_id == tg_id))
        if user.sub == 'yes':
            return True
        return False

async def get_text(id_):
    async with async_session() as session:
        text = await session.scalar(Select(TextDesc).where(TextDesc.id == id_))
        return text

async def update_sub(tg_id, price):
    async with async_session() as session:
        sub = await session.scalar(Select(User).where(User.user_id == tg_id))
        sub.sub = 'yes'
        user_ref = await session.scalar(Select(Referal).where(Referal.ref_id == tg_id))
        if user_ref:
            user_ref.price = int(price)//2
        await session.commit()


async def get_users():
    async with async_session() as session:
        users = await session.scalars(Select(User))
        return list(users)

async def get_referals(tg_id):
    async with async_session() as session:
        referals = list(await session.scalars(Select(Referal).where(Referal.user_id == tg_id)))
        # ref_have = list(filter(lambda x: x == 'yes', list(await session.scalars(Select(User.sub).where(User.user_id.in_(referals))))))
        return referals


async def add_referal(user_id, ref_id):
    async with async_session() as session:
        if await session.scalar(Select(Referal).where(Referal.ref_id == ref_id)):
            return False
        session.add(Referal(user_id=user_id, ref_id=ref_id))
        await session.commit()


async def get_all_text():
    async with async_session() as session:
        texts = await session.scalars(Select(TextDesc))
        return texts

async def edit_text(id_, desc):
    async with async_session() as session:
        text = await session.scalar(Select(TextDesc).where(TextDesc.id == id_))
        text.text = desc
        await session.commit()

