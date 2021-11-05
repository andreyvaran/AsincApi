import json

from aiohttp import web

from messenger.api import views
from messenger.api import search

routes = web.RouteTableDef()


@routes.post('/v1/db_change')
async def post_db_con(request: web.Request) -> web.Response:
    try:
        data = request.query['conection']
        if data in ['true', 'True', True, 1, '1']:
            request.app['db_con'] = True
        else:
            request.app['db_con'] = False

        return web.Response(status=200, body=json.dumps({"message": 'conection was updated'}),
                            content_type='application/json')
    except Exception as e:
        print(e)
        return web.Response(status=400, body=json.dumps({'message': 'bad-parameters'}),
                            content_type='application/json')


@routes.get('/v1/ping_db')
async def check_db_con(request: web.Request) -> web.Response:
    if request.app['db_con'] == True:
        return web.Response(status=200, body=json.dumps({'message': "successfully connected"}),
                            content_type='application/json')
    else:
        return web.Response(status=503, body=json.dumps({'message': "can't connect to db"}),
                            content_type='application/json')


def setup_routes(app) -> None:
    app.router.add_view(r"/v1/chats", views.Chat)
    app.router.add_view(r"/v1/chats/", views.Chat)

    app.router.add_view(r"/v1/chats/{chat_name}/users", views.User)
    app.router.add_view(r"/v1/chats/{chat_name}/users/", views.User)
    #
    app.router.add_view(r"/v1/chats/{chat_name}/messages", views.Message)
    app.router.add_view(r"/v1/chats/{chat_name}/messages/", views.Message)
    #
    app.router.add_view(r'/v1/autorisation', views.Autorisation)
    app.router.add_view(r'/v1/autorisation/', views.Autorisation)

    app.router.add_view(r'/v1/chats/search', search.MakeTask)
    app.router.add_view(r'/v1/chats/search/', search.MakeTask)

    app.router.add_view(r'/v1/chats/search/status/{task_id}', search.StatusTask)
    app.router.add_view(r'/v1/chats/search/status/{task_id}/', search.StatusTask)

    app.router.add_view(r'/v1/chats/search/{task_id}/messages', search.TaskContent)
    app.router.add_view(r'/v1/chats/search/{task_id}/messages/', search.TaskContent)

    app.add_routes(routes)
