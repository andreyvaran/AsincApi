DATABASE = 'usersettings'
IS_CONECTED_DB = True
class DBExeption(Exception):
    pass

URL_TO_SQLALCHEMY = 'postgresql+psycopg2://postgres:Krasnin@localhost/usersettings'