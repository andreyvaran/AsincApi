from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from .models import UserChat, UserSettings, Chats, Messages
import asyncio
from sqlalchemy import create_engine

import uuid


async def add_user_to_db(user, app, user_id):
    engine = app['engine']
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            session.add(
                UserSettings(id=user_id,
                             username=user.username,
                             password=user.password,
                             timezone=user.timezone))


async def add_chat_to_db(app, chat_id, chat_name, admin_id, user_limit=100):
    engine = app['engine']
    # admin_id = uuid.UUID(str(admin_id))
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            # try:
            if admin_id != app['admin_uuid']:
                session.add(
                    Chats(id=chat_id,
                          chat_name=chat_name,
                          admin_id=admin_id,
                          user_limit=user_limit)
                )
                session.add(
                    UserChat(
                        chat_id=chat_id,
                        user_id=app['admin_uuid'])
                )
            else:
                session.add(
                    Chats(id=chat_id,
                          chat_name=chat_name,
                          admin_id=admin_id,
                          user_limit=user_limit)
                )


async def add_to_user_into_chat(app, user_id, chat_id, user_name):
    engine = app['engine']

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async_session = app['async_session']
    # В случае если пользователь не указал свое имя для чата , его имя будет именем пользователя
    if user_name in [None, '']:
        async with async_session() as session:
            query = select(UserSettings).where(UserSettings.id == user_id)
            result = await session.execute(query)
            result = result.scalars().first()
        user_name = result.username

    async with async_session() as session:
        async with session.begin():
            # try:
            session.add(
                UserChat(
                    chat_id=chat_id,
                    user_id=user_id,
                    user_name=user_name)
            )


async def post_message(app, user_id, chat_id, text):
    engine = app['engine']

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            # try:
            session.add(
                Messages(
                        chat_id=chat_id,
                        user_id=user_id,
                        text=text)
                )

def post_admin(db_url , admin_name, password , admin_uuid , timezone = 3):

    engine = create_engine(db_url,echo = True)
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind = engine)
    session = session()
    session.add(
        UserSettings(id=admin_uuid,
                     username=admin_name,
                     password=password,
                     timezone=timezone))

    session.commit()

# async def add_bot_to_db(app):
#     engine = app['engine']
#     async_session = sessionmaker(
#         engine, expire_on_commit=False, class_=AsyncSession
#     )
#     async with async_session() as session:
#         async with session.begin():
#             try:
#                 session.add(UserSettings(username='bot', password='qwerty', timezone=3))
#             except Exception as e:
#                 pass
#                 # print(e)
#         # bot = UserSettings(id = -1 , username = 'bot' , password = 'qwerty' , timezone = 3 )
#
# # asyncio.run(add_bot_to_db())
# #
