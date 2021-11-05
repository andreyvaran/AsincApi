import uuid
from typing import Optional

from pydantic import validator, BaseModel, Field, ValidationError


class SchemaLimit(BaseModel):
    limit: int
    From: Optional[int] = Field(alias="from", default=None)

    @validator("limit")
    def in_between(cls, v):
        if v < 1 or v > 1000:
            raise ValidationError(f'The limit={v} is not in the range from 1 to 10000')
        return v


class SchemaMessage(BaseModel):
    text: str = Field(alias="message", default=None)


class SchemaChat(BaseModel):
    chat_name: str = Field(alias="chat_name", default=None)

    @validator('chat_name')
    def try_valid(cls, chat_name):
        if len(chat_name) > 255:
            raise ValidationError('To many symbols in chat_id')
        return chat_name

class SchemaTask(BaseModel):
    task_id: str = Field(alias='task_id',  default=None)


class SchemaUser(BaseModel):
    user_name: str = Field(alias="user_name", default=None)

    @validator('user_name')
    def try_valid(cls, user_name):
        if len(user_name) > 255:
            raise ValidationError('To many symbols in user_name ')
        return user_name


class SchemaUserAutorisatin(BaseModel):
    username: str = Field(alias="username", default=None)
    password: str = Field(alias="password", default=None)
    timezone: float = Field(alias='timezone', default=3)

    @validator('username')
    def try_valid(cls, username):
        if len(username) > 255:
            raise ValidationError('To many symbols in user_name ')
        return username

    @validator('password')
    def valid_password(cls, password):
        if len(password) < 8:
            raise ValidationError('Password must be more that 8 symbols ')
        return password
