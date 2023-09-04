
from models.dvd_model import Base
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session, sessionmaker
import asyncio

engine = create_async_engine("mysql+aiomysql://root@localhost:3306/nefos23dvd", echo=True)

async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def init_db():
    asyncio.run(init_models())
   
    db_session.commit()
    print("Initialized the db")

db_session = scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit = False
        )
    )



def get_db_session():
    return db_session