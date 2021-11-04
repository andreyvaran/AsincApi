import datetime
from datetime import datetime
import messenger
from messenger.tools import datetime_with_delta, get_str_hellow

from messenger.secod_base.users_cvc import get_settings_by_user_id_csv
from aiohttp import web, web_exceptions
from pydantic import ValidationError
import json
# from messenger.Globals import DBException

@web.middleware
async def midlware_no_db(request, handler):
    try:
        temp = await handler(request)
    except messenger.Globals.DBExeption as e :

        user_id = request.headers.get('user_id', '')

        time_exeption = datetime.now()
        dict_user = get_settings_by_user_id_csv('../users.csv', user_id)
        time = datetime_with_delta(dict_user['time'])
        text = get_str_hellow(time) + ' ' + dict_user['username'] + '  no conection to DB '

        temp = web.Response(status=500, body=json.dumps({'message': text,
                                                         'time': str(time_exeption)}),
                            content_type='application/json')

    except ValidationError:
        temp =  web.Response(status=400, body=json.dumps({'message': 'bad-parameters'}),
                            content_type='application/json')
    except OverflowError:
        temp =  web.Response(status=400, body=json.dumps({'message': 'bad-parameters'}),
                             content_type='application/json')

    return temp