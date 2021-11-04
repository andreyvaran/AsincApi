from aiohttp import web
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sqlalchemy

from cnf import DB_CONNECTION_STR, DB_CONNECTION_STR_SYNC, AUTH_DISABLED

from messenger.db.post_data import post_admin
from messenger.secod_base.users_cvc import set_one_user


def setup_routes(app: web.Application) -> None:
    from messenger.api.routes import setup_routes as sr
    sr(app)


#
def setup_middlewares(app: web.Application) -> None:
    from messenger.api.midlware import midlware_no_db
    app.middlewares.append(midlware_no_db)


from aiohttp.abc import AbstractAccessLogger
from datetime import datetime


class AccessLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        self.logger.info(f' {datetime.now()} '
                         f'" {request.method} {request.path} '
                         # f'header {request.headers}'
                         f'query {request.query}'
                         f'done in {time}s: {response.status}'
                         )


# 'postgresql+asyncpg://postgres:Krasnin@localhost:5400/chatbot'
def main() -> None:
    app = web.Application()
    app['db_con'] = True
    app['db_url'] = DB_CONNECTION_STR
    app['db_url_sync'] = DB_CONNECTION_STR_SYNC
    app['engine'] = create_async_engine(app['db_url'], echo=True)
    app['async_session'] = sessionmaker(app['engine'], expire_on_commit=False, class_=AsyncSession)
    # todo get admin settings from .env
    app['admin_username'] = 'perevoshikov'
    app['admin_password'] = 'qwertyuiop'
    app['admin_uuid'] = '0f87bf68-3144-4a2b-a89c-2583120e4fb0'
    app['AUTH_DISABLED'] = AUTH_DISABLED in ['True' , 'true']
    try:
        # Если пользователь админ не создан , то создает его при запуске
        post_admin(app['db_url_sync'], app['admin_username'], app['admin_password'], app['admin_uuid'], 3)
    except sqlalchemy.exc.IntegrityError:
        print('Admin alredy existes')

    # app.cache =
    setup_routes(app)
    setup_middlewares(app)
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, access_log_class=AccessLogger, port=8080)


if __name__ == '__main__':
    main()
