from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

from .models import UserSettings, Messages, UserChat
import asyncio
from sqlalchemy import desc, func


async def get_user_id(app, user_id):
    async_session = app['async_session']
    async with async_session() as session:
        query = select(UserSettings).where(UserSettings.id == user_id)
        result = await session.execute(query)
        # print(result.scalars().all())
        # print(type(result.scalars().all()))
        #
        # for i in result.scalars():
        #     print(i)
        #     print(type(i))
        result = result.scalars().first()
    return result


async def get_all_user(app) -> list:
    async_session = app['async_session']
    async with async_session() as session:
        query = select(UserSettings)
        result = await session.execute(query)
        result = result.scalars()
    res_arr = []
    for i in result:
        res_arr.append({'id': i.id,
                        'username': i.username
                        })
    return res_arr


async def get_from_first_message(app, chat_id, limit):
    async_session = app['async_session']
    async with async_session() as session:
        query = select(Messages).where(Messages.chat_id == chat_id).order_by(
            Messages.send_time.desc()).limit(limit)
        result = await session.execute(query)
        result = result.scalars()
    res_arr = []
    last_id = -1
    for msg in result:
        res_arr.insert(0, msg.text)

        last_id = msg.id
    return res_arr, last_id


async def get_from_first_message_by_users(app, user_id, chat_id, limit):
    async_session = app['async_session']
    async with async_session() as session:
        query = select(Messages).where(
            Messages.user_id == user_id, Messages.chat_id == chat_id).order_by(
            Messages.send_time.desc()).limit(limit)
        result = await session.execute(query)
        result = result.scalars()
    res_arr = []
    limit = -1
    for msg in result:
        res_arr.insert(0, msg.text)

        if last_id < msg.id:
            last_id = msg.id
    return res_arr, last_id


async def get_from_id_message(app, chat_id, limit, from_time):
    async_session = app['async_session']
    async with async_session() as session:
        query = select(Messages).where(Messages.chat_id == chat_id, Messages.send_time >= from_time).order_by(
            Messages.send_time.desc()).limit(limit)
        result = await session.execute(query)
        result = result.scalars()
    res_arr = []
    last_id = -1
    for msg in result:
        res_arr.insert(0, msg.text)

        if last_id < msg.id:
            last_id = msg.id

    return res_arr, last_id


async def get_task_search(app, user_id, message):
    async_session = app['async_session']
    async with async_session() as session:
        query = select(UserChat).where(UserChat.user_id == user_id)
        temp = await session.execute(query)
        temp = temp.scalars().all()
        res = []

        for i in temp:
            query = select(Messages).where(Messages.user_id == user_id, Messages.chat_id == i.chat_id,
                                           func.strpos(Messages.text, message.text) > 0)
            temp1 = await session.execute(query)

            res += temp1.scalars().all()
        await asyncio.sleep(60)

    return res
