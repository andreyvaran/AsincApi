from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, INTEGER
import uuid

Base = declarative_base()


class UserSettings(Base):
    __tablename__ = 'users_settings'

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String, nullable=False)
    timezone = Column(Float, default=3, nullable=False)
    password = Column(String, server_default="password", nullable=False)
    # last_time_online = relationship('LastTimeOnline')


class Chats(Base):
    __tablename__ = 'chats_settings'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chat_name = Column(String(255), nullable=False, unique=True)
    user_limit = Column(Integer, default=100)
    admin_id = Column(UUID(as_uuid=True), nullable=False)
    messages = relationship('Messages')


class UserChat(Base):
    __tablename__ = 'users_chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chats_settings.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users_settings.id', ondelete="CASCADE"), nullable=False)
    user_name =  Column(String , nullable=True)


class Messages(Base):
    __tablename__ = 'messenges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users_settings.id', ondelete="CASCADE"), nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chats_settings.id', ondelete="CASCADE"), nullable=False)
    send_time = Column(DateTime, default=func.now())


#
class LastTimeOnline(Base):
    __tablename__ = 'online'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users_settings.id', ondelete="CASCADE"), nullable=False)
    time = Column(DateTime)

#
#
# Base.metadata.drop_all(engine)
#
# Base.metadata.create_all(bind=engine)
#
#
