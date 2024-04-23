from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger, String, ForeignKey, Text, Integer, Date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import datetime


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=False)

async_session = async_sessionmaker(engine)
class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(30))
    sub: Mapped[str] = mapped_column(String(10), default='no')



class Referal(Base):
    __tablename__ = 'referals'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    ref_id = mapped_column(BigInteger)
    price = mapped_column(Integer, default=0)
    date_sub = mapped_column(Date, default=datetime.datetime.now())
class TextDesc(Base):
    __tablename__ = 'texts'

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(Text)

    name_text: Mapped[str] = mapped_column(String(20))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

