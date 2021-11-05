import asyncio
import json
import uuid
from datetime import datetime
from functools import lru_cache
from async_lru import alru_cache
from aiohttp import web

# from messenger.messenger.db.check_db import check_db ,check_db_for_smart

from messenger.schema.schema import SchemaChat, SchemaUser, SchemaMessage, \
    SchemaLimit, SchemaUserAutorisatin, SchemaTask
from pydantic import ValidationError
from messenger.secod_base.users_cvc import set_one_user
from messenger.Globals import DBExeption
from messenger.db.post_data import add_user_to_db, add_chat_to_db, add_to_user_into_chat, post_message, post_admin
from messenger.db.check_is import check_chat_name, check_user_id, check_chat_id, check_user_in_chat, \
    check_from_in_messages
from messenger.db.get_data import get_user_id, get_from_first_message, get_from_id_message, get_task_search
from uuid import uuid4
import sqlalchemy


class MakeTask(web.View):
    '''http://0.0.0.0:8080/v1/chats/search'''

    async def post(self):
        if not self.request.app['db_con']:
            raise DBExeption
        # Check user in db
        user_id = self.request.headers.get('user_id', '')
        if user_id != '':
            user_id = uuid.UUID(user_id)
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']

        if await check_user_id(self.request.app, user_id) == False:
            return web.Response(status=401,
                                body=json.dumps({'message': 'U cant read messenges until you registred'}),
                                content_type='application/json')
        print(self.request.app.task_dict)
        data = await self.request.json()
        message = SchemaMessage.parse_obj(data)
        if message.text == None:
            raise OverflowError

        task = asyncio.create_task(get_task_search(self.request.app, user_id, message))
        task_id = uuid.uuid4()
        self.request.app.task_dict[task_id] = [task, datetime.now(), user_id]

        return web.Response(status=200,
                            body=json.dumps({'task_id': str(task_id)}),
                            content_type='application/json')


class StatusTask(web.View):
    async def get(self):
        if not self.request.app['db_con']:
            raise DBExeption

        task_id = uuid.UUID(SchemaTask.parse_obj(self.request.match_info).task_id)
        # time = datetime.now()

        if task_id not in self.request.app.task_dict.keys():
            return web.Response(status=404,
                                body=json.dumps({'message': 'task not found'}),
                                content_type='application/json')

        delta = datetime.now() - self.request.app.task_dict[task_id][1]

        if delta.seconds > 600:
            self.request.app.task_dict[task_id][0].cancel()
            del self.request.app.task_dict[task_id]
            return web.Response(status=200,
                                body=json.dumps({'status': 'cancelled( Runtime error more than 5 seconds)'}),
                                content_type='application/json')

        try:
            task = self.request.app.task_dict[task_id][0].result()

            return web.Response(status=200,
                                body=json.dumps({'status': 'done'}),
                                content_type='application/json')
        except asyncio.CancelledError:
            return web.Response(status=200,
                                body=json.dumps({'status': 'cancelled'}),
                                content_type='application/json')
        except asyncio.InvalidStateError:
            return web.Response(status=200,
                                body=json.dumps({'status': 'in process'}),
                                content_type='application/json')


#

class TaskContent(web.View):
    @alru_cache(maxsize=32)
    async def get(self):
        if not self.request.app['db_con']:
            raise DBExeption
        # Check user in db
        user_id = self.request.headers.get('user_id', '')
        if user_id != '':
            user_id = uuid.UUID(user_id)
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']

        if await check_user_id(self.request.app, user_id) == False:
            return web.Response(status=401,
                                body=json.dumps({'message': 'U cant read messenges until you registred'}),
                                content_type='application/json')
        task_id = uuid.UUID(SchemaTask.parse_obj(self.request.match_info).task_id)

        if task_id not in self.request.app.task_dict.keys():
            return web.Response(status=404,
                                body=json.dumps({'message': 'task not found'}),
                                content_type='application/json')

        if self.request.app.task_dict[task_id][2] != user_id:
            return web.Response(status=400,
                                body=json.dumps({'message': 'U cant read enemy task'}),
                                content_type='application/json')

        schema_message = SchemaLimit.parse_obj(self.request.query)
        # user_id = uuid.UUID(user_id)
        messages_list = []

        try:
            result = self.request.app.task_dict[task_id][0].result()
            message_list = []

            last_id = result[0].id
            if schema_message.limit == None:
                raise OverflowError

            if schema_message.From == None:
                for i in result[0:schema_message.limit]:
                    message_list.append({"text": i.text, "chat_id": str(i.chat_id)})

                print(message_list)

                return web.Response(status=200,
                                    body=json.dumps({'messages': message_list,
                                                     "next": {
                                                         "iterator": str(last_id)
                                                     }}),
                                    content_type='application/json')
            else:
                if schema_message.From not in list(map(lambda x: x.id, result)):
                    return web.Response(status=404, body=json.dumps({'Error': 'no from in messages'}),
                                        content_type='application/json')
                for i in result[0:schema_message.limit]:
                    if i.id >= schema_message.From:
                        message_list.append({"text": i.text, "chat_id": str(i.chat_id)})
                print(message_list)
                return web.Response(status=200,
                                    body=json.dumps({'messages': message_list,
                                                     "next": {
                                                         "iterator": str(last_id)
                                                     }}),
                                    content_type='application/json')

        except asyncio.InvalidStateError:
            return web.Response(status=200,
                                body=json.dumps({'Message': 'Cant read until task in process'}),
                                content_type='application/json')
