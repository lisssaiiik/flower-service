from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, Header, Request, Response
from users_service.auth import authenticate_user, create_access_token, get_password_hash
from users_service.dao import UsersDAO
from users_service.dependencies import get_current_user
from users_service.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from users_service.schemas import SUserAuth, SUserInfo, SUserLogin, SUserUpdate

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    """Функция, регистрирующая пользователя"""
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password,
                       first_name=user_data.first_name, last_name=user_data.last_name,
                       middle_name=user_data.middle_name, phone_number=user_data.phone_number,
                       date_of_birth=user_data.date_of_birth, address=user_data.address)


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    """Функция позволяет пользователю авторизоваться"""
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("flower_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    """Функция, с помощью которой пользователь выходит из системы. Удаляет действующую куку"""
    response.delete_cookie("flower_access_token")


@router.get("/me", response_model=SUserInfo, summary="Returns info about the user")
async def get_user_info(request: Request, token: Annotated[str | None, Header()] = None):
    """Метод, возвращающий информацию о пользователе(id, email, пароль и роль)"""
    if not token:
        token = request.cookies.get("flower_access_token")
    current_user = get_current_user(token)
    return await current_user


@router.patch("/update")
async def update_user(user_update: SUserUpdate, current_user = Depends(get_current_user)):
    """Метод, обновляющий данные пользователя"""
    if user_update.first_name is not None:
        await UsersDAO.update(current_user.id, first_name=user_update.first_name)
    if user_update.last_name is not None:
        await UsersDAO.update(current_user.id, last_name=user_update.last_name)
    if user_update.middle_name is not None:
        await UsersDAO.update(current_user.id, middle_name=user_update.middle_name)
    if user_update.address is not None:
        await UsersDAO.update(current_user.id, address=user_update.address)
    if user_update.birth_date is not None and user_update.birth_date < date.today():
        await UsersDAO.update(current_user.id, date_of_birth=user_update.birth_date)
    return {"status": "success"}
