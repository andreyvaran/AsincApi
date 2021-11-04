import json
import uuid
from datetime import datetime
from functools import lru_cache

from aiohttp import web

# from messenger.messenger.db.check_db import check_db ,check_db_for_smart

from messenger.schema.schema import SchemaChat, SchemaUser, SchemaMessage, \
    SchemaLimit, SchemaUserAutorisatin
from pydantic import ValidationError
from messenger.secod_base.users_cvc import set_one_user
from messenger.Globals import DBExeption
from messenger.db.post_data import add_user_to_db, add_chat_to_db, add_to_user_into_chat, post_message, post_admin
from messenger.db.check_is import check_chat_name, check_user_id, check_chat_id, check_user_in_chat, \
    check_from_in_messages
from messenger.db.get_data import get_user_id, get_from_first_message, get_from_id_message
from uuid import uuid4
import sqlalchemy


class Chat(web.View):
    '''  Add chat to user
    http://localhost:8080/v1/chats
    headers :
    '''

    @lru_cache(maxsize=128)
    async def post(self):

        if not self.request.app['db_con']:
            raise DBExeption
        # Check user in db
        user_id = self.request.headers.get('user_id', '')
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']

        if await check_user_id(self.request.app, user_id) == False:
            return web.Response(status=401,
                                body=json.dumps({'message': 'U cant read messenges until you registred'}),
                                content_type='application/json')

        data = await self.request.json()

        schema_chat = SchemaChat.parse_obj(data)

        if schema_chat.chat_name is None:
            raise OverflowError

        chat_id = uuid4()
        user_id = uuid.UUID(user_id)
        try:

            await add_chat_to_db(self.request.app, chat_id, schema_chat.chat_name, user_id)
            await add_to_user_into_chat(self.request.app, user_id, chat_id, '')
            if self.request.app['AUTH_DISABLED'] == False:
                # add admin что бы при отключенной авторизации можно было счотреть и читать все сообщения в чатах
                await add_to_user_into_chat(self.request.app, self.request.app['admin_uuid'], chat_id, '')

        except sqlalchemy.exc.IntegrityError:
            return web.Response(status=400,
                                body=json.dumps({'message': 'This name is already exist '}),
                                content_type='application/json')

        # todo  get  limit user in query

        return web.Response(status=201,
                            body=json.dumps({'chat_name': schema_chat.chat_name,
                                             'id': str(chat_id)}),
                            content_type='application/json')


class User(web.View):
    ''' Add user to chat
    http://localhost:8080/v1/chats/{chat_name}/users
    query =
    headers :
    '''

    @lru_cache(maxsize=128)
    async def post(self):

        if not self.request.app['db_con']:
            raise DBExeption
        user_id = self.request.headers.get('user_id', '')
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']

        if await check_user_id(self.request.app, user_id) == False:
            return web.Response(status=401,
                                body=json.dumps({'message': 'U cant read messenges until you registred'}),
                                content_type='application/json')

        tmp_chat = SchemaChat.parse_obj(self.request.match_info)

        chat_in, chat_id = await check_chat_name(self.request.app, tmp_chat.chat_name)

        user_alredy_in_chat = check_user_in_chat(self.request.app, user_id, chat_id)
        if await user_alredy_in_chat:
            return web.Response(status=201,
                                body=json.dumps({'message': 'This user is already present in the chat',
                                                 'chat_name': tmp_chat.chat_name,
                                                 'chat_id': str(chat_id)}),
                                content_type='application/json')
        if chat_in:
            data = await self.request.json()
            create_user = SchemaUser.parse_obj(data)
            await add_to_user_into_chat(self.request.app, user_id, chat_id, create_user.user_name)
            return web.Response(status=201,
                                body=json.dumps({'user_name': create_user.user_name,
                                                 'user_id': user_id,
                                                 'chat_name': tmp_chat.chat_name,
                                                 'chat_id': str(chat_id)}),
                                content_type='application/json')
        else:
            return web.Response(status=404,
                                body=json.dumps({'Error': 'no chat this name'}),
                                content_type='application/json')


class Message(web.View):
    @lru_cache(maxsize=128)
    async def post(self):
        '''
        Send message from user to chat
        post response to
        http://localhost:8080/v1/chats/{chat_id}/messages?user_id=112
        '''

        if not self.request.app['db_con']:
            raise DBExeption
        user_id = self.request.headers.get('user_id', '')
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']

        tmp_chat = SchemaChat.parse_obj(self.request.match_info)

        if tmp_chat.chat_name == None:
            raise OverflowError

        # check chat id in DB
        is_chat_avel, chat_id = await check_chat_name(self.request.app, tmp_chat.chat_name)
        if is_chat_avel:
            if await check_user_in_chat(self.request.app, user_id, chat_id):

                user_id = uuid.UUID(user_id)
                data = await self.request.json()
                message = SchemaMessage.parse_obj(data)

                if message.text == None:
                    raise ValueError
                await post_message(self.request.app, user_id, chat_id, message.text)
                return web.Response(status=201, body=json.dumps({'message': 'Success'}),
                                    content_type='application/json')

            else:
                return web.Response(status=404, body=json.dumps({'Error': 'no user in  this chat'}),
                                    content_type='application/json')
        else:
            return web.Response(status=404, body=json.dumps({'Error': 'no chat with this name'}),
                                content_type='application/json')

    @lru_cache(maxsize=128)
    async def get(self):
        user_id = self.request.headers.get('user_id', '')
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']

        if not self.request.app['db_con']:
            raise DBExeption

        # Валидирует данные id чата
        schema_chat = SchemaChat.parse_obj(self.request.match_info)

        is_chat_avel, chat_id = await check_chat_name(self.request.app, schema_chat.chat_name)
        if is_chat_avel:
            if await check_user_in_chat(self.request.app, user_id, chat_id):
                schema_message = SchemaLimit.parse_obj(self.request.query)
                user_id = uuid.UUID(user_id)
                messages_list = []

                if schema_message.limit == None:
                    raise OverflowError
                if schema_message.From == None:
                    # todo C 1 сообщения в чате
                    messages_list, schema_message.From = await get_from_first_message(self.request.app,
                                                                                      chat_id,
                                                                                      schema_message.limit)
                    if schema_message.From == -1:
                        schema_message.From = 'No messages in chat'
                else:
                    # Cделать проверку что from есть в сообщениях
                    # Если она есть , то вывести сообщения, иначе вывести ошибку 404 нет такого
                    from_aveliable, from_time = await check_from_in_messages(self.request.app, schema_message.From,
                                                                             chat_id)
                    if from_aveliable:
                        messages_list, schema_message.From = await get_from_id_message(self.request.app,
                                                                                       chat_id,
                                                                                       schema_message.limit,
                                                                                       from_time)
                    else:
                        return web.Response(status=404, body=json.dumps({'Error': 'no from in this name'}),
                                            content_type='application/json')

                messages = {
                    "messages": messages_list,
                    'next': schema_message.From
                }
                result = json.dumps(messages)

                return web.Response(status=200, body=result,
                                    content_type='application/json')
            else:
                return web.Response(status=401,
                                    body=json.dumps({'message': 'U cant read messenges until you registred'}),
                                    content_type='application/json')
        else:
            return web.Response(status=404, body=json.dumps({'Error': 'no chat this name'}),
                                content_type='application/json')


class Autorisation(web.View):
    ''' Autorisation
    http://localhost:8080/v1/autorisation
    headers :
    '''

    async def post(self):
        try:
            if not self.request.app['db_con']:
                raise DBExeption
            user = SchemaUserAutorisatin.parse_obj(self.request.headers)

            if user.username is None or user.password is None:
                raise ValidationError
            user_id = uuid4()
            await add_user_to_db(user, self.request.app, user_id)
            set_one_user('../users.csv', user, user_id)
            return web.Response(status=200,
                                body=json.dumps({'message': 'Successfully logged in',
                                                 'username': user.username}),
                                content_type='application/json')
        except ValidationError as e:
            return web.Response(status=400,
                                body=json.dumps({'message': str(e)}),
                                content_type='application/json')

    # Get user by id
    async def get(self):
        if not self.request.app['db_con']:
            raise DBExeption
        user_id = self.request.headers.get('id', -1)
        res = await check_user_id(self.request.app, user_id)
        if res:

            res2 = await get_user_id(self.request.app, user_id)

            return web.Response(status=200,
                                body=json.dumps({'message': 'Find user ',
                                                 'username': res2.username}),
                                content_type='application/json')
        else:
            return web.Response(status=404,
                                body=json.dumps({'message': 'No user with user_id',
                                                 'user_id': user_id}),
                                content_type='application/json')
