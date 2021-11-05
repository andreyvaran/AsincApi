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

        task =  asyncio.create_task(get_task_search(self.request.app , user_id , message))
        task_id = uuid.uuid4()
        self.request.app.task_dict[task_id] = [task ,datetime.now(), user_id]

        return web.Response(status=200,
                            body=json.dumps({'task_id': str(task_id)}),
                            content_type='application/json')


class StatusTask(web.View):
    async def get(self):
        if not self.request.app['db_con']:
            raise DBExeption
        # Check user in db
        # user_id = self.request.headers.get('user_id', '')
        if self.request.app['AUTH_DISABLED']:
            user_id = self.request.app['admin_uuid']
        task_id = uuid.UUID(SchemaTask.parse_obj(self.request.match_info).task_id)

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
            return  web.Response(status=200,
                                       body=json.dumps({'status': 'in process'}),
                                       content_type='application/json')

