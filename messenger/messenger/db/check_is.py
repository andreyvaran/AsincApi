import datetime

from sqlalchemy.sql import select
from .models import UserSettings, Chats , UserChat , Messages


async def check_user_id(app, user_id) -> bool:
    if user_id == '' :
        return False
    async_session = app['async_session']
    async with async_session() as session:
        query = select(UserSettings).where(UserSettings.id == user_id)
        result = await session.execute(query)
        result = result.scalars().first()
    if result is not None:
        return True
    else:
        return False

async def check_user_in_chat(app , user_id ,  chat_id) -> bool :
    if user_id == '' :
        return False
    async_session = app['async_session']
    async with async_session() as session:
        query = select(UserChat).where(UserChat.chat_id == chat_id , UserChat.user_id == user_id )
        result = await session.execute(query)
        result = result.scalars().first()

    if result is not None:

        return True
    else:
        return False

async def check_chat_id(app, chat_id) -> bool:
    if len(str(chat_id)) < 35:
        return False
    print(123)
    async_session = app['async_session']
    async with async_session() as session:
        query = select(Chats).where(Chats.id == chat_id)
        result = await session.execute(query)
        result = result.scalars().first()
    if result is not None:
        return True
    else:
        return False

async def check_chat_name(app, chat_name):
    if chat_name == '':
        return False , 0
    async_session = app['async_session']
    async with async_session() as session:
        query = select(Chats).where(Chats.chat_name == chat_name)
        result = await session.execute(query)
        result = result.scalars().first()
    if result is not None:
        return True, result.id
    else:
        return False , 0

async def check_from_in_messages(app , from_id , chat_id):
    async_session = app['async_session']
    async with async_session() as session:
        query = select(Messages).where(Messages.chat_id == chat_id , Messages.id == from_id)
        result = await session.execute(query)
        result = result.scalars().first()
    if result is not None:
        return True , result.send_time
    else:
        return  False, datetime.datetime.now()
