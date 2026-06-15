# import os
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from dotenv import load_dotenv, find_dotenv
# from database.models import Base
#
# load_dotenv(find_dotenv())
#
# DB_URL = os.getenv("DE_LITE")
#
# engine = create_async_engine(url=DB_URL, echo=True)
#
# session_loop = async_sessionmaker(class_=AsyncSession, bind=engine, expire_on_commit=False)
#
# async def create_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# async def drop_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
