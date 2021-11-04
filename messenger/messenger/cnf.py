#cat routes.py
from dotenv import load_dotenv
import os

load_dotenv()

# load_dotenv('messenger/messenger/.env')
# print(load_dotenv)
# DB_USER = os.getenv('POSTGRES_USER')
# print(DB_USER)

# 'postgresql+asyncpg://postgres:Krasnin@localhost:5400/chatbot'
DB_USER = os.getenv('POSTGRES_USER')
print(DB_USER)
# load_dotenv.__get__('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PWD')
DB_HOSTS = os.getenv('POSTGRES_HOSTS')
DB_NAME = os.getenv('POSTGRES_DB')
AUTH_DISABLED = os.getenv('AUTH_DISABLED')
# print(* os.environ)

DB_CONNECTION_STR = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOSTS}:5400/{DB_NAME}"
DB_CONNECTION_STR_SYNC = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOSTS}:5400/{DB_NAME}"
print(DB_CONNECTION_STR)
