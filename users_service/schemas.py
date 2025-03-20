from datetime import date
from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):  # схемы нужны для валидации данных
    """Схема для аутенфикации пользователя"""
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    middle_name: str = Field(min_length=2)
    phone_number: str = Field(min_length=11)
    date_of_birth: date
    address: str


class SUserLogin(BaseModel):  # схемы нужны для валидации данных
    """Схема для логина"""
    email: EmailStr
    password: str = Field(min_length=8)


class SUserInfo(BaseModel):
    """Схема инфы о пользователе"""
    id: int
    email: str
    first_name: str 
    last_name: str
    middle_name: str 
    phone_number: str
    date_of_birth: date
    address: str
    role: str


class SUserUpdate(BaseModel):
    first_name: str = Field(default=None, min_length=2)
    last_name: str = Field(default=None, min_length=2)
    middle_name: str = Field(default=None, min_length=2)
    birth_date: date = Field(default=None)
    address: str = Field(default=None, min_length=2)
