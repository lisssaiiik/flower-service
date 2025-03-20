from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Header, Request
import requests
from cart_service.dao import CartDAO, StarsDAO
from cart_service.dependencies import get_current_user
from cart_service.exceptions import IncorrectFlowerIDException
from cart_service.schemas import SStars


router = APIRouter(prefix="/cart", tags=["Корзина"])
stars_router = APIRouter(prefix="/stars", tags=["избранное"])


@router.post("/{bouquet_id}")
async def add_to_cart(bouquet_id: int, quantity: int, current_user = Depends(get_current_user)):
    """Добавление букета в корзину"""
    await CartDAO.add(bouquet_id=bouquet_id, quantity=quantity, user_id=current_user['id'])


@router.delete("/{bouquet_id}")
async def remove_from_cart(cart_item_id: int, current_user = Depends(get_current_user)):
    """Удаление букета из корзины"""
    await CartDAO.delete(id=cart_item_id, user_id=current_user['id'])


@router.patch("/{cart_item_id}/inc")
async def increment_cart_item(cart_item_id: int, current_user = Depends(get_current_user)):
    """Увеличить количество букетов в корзине на 1"""
    cart_item = await CartDAO.find_by_id(cart_item_id)
    await CartDAO.update(cart_item_id=cart_item_id, user_id=current_user['id'],
                         quantity=cart_item.quantity + 1)

@router.patch("/{cart_item_id}/dec")
async def decrement_cart_item(cart_item_id: int, current_user = Depends(get_current_user)):
    """Уменьшить количество букетов в корзине на 1"""
    cart_item = await CartDAO.find_by_id(cart_item_id)
    await CartDAO.update(cart_item_id=cart_item_id, user_id=current_user['id'],
                         quantity=cart_item.quantity - 1)
    cart_item = await CartDAO.find_by_id(cart_item_id)
    if cart_item.quantity <= 0:
        await CartDAO.delete(id=cart_item_id, user_id=current_user['id'])

@router.get("/")
async def view_cart(current_user = Depends(get_current_user)):
    """Просмотр корзины"""
    return await CartDAO.find_all(user_id=current_user['id'])


@router.get("/{cart_id}")
async def get_item_cart(cart_id: int, request: Request,
                        token: Annotated[str | None, Header()] = None):
    if token is None:
        token = request.cookies.get("flower_access_token")
    headers = {'accept': 'application/json', 'token': token}
    user_response = requests.get('http://127.0.0.1:8000/auth/me', headers=headers, timeout=10)
    if user_response.status_code == 401:
        raise HTTPException(status_code=401, detail="Not authorized")
    return await CartDAO.find_one_or_none(id=cart_id, user_id=user_response.json()['id'])


@stars_router.get("/", response_model=List[SStars])
async def get_stars(current_user = Depends(get_current_user)):
    """Возвращает "Избранное" пользователя"""
    stars = await StarsDAO.find_all(user_id=current_user['id'])
    return stars


@stars_router.post("/{flower_id}")
async def add_bouquet_to_stars(flower_id: int, current_user = Depends(get_current_user)):
    """Добавление букета в -Избранное-"""
    headers = {'accept': 'application/json'}
    response = requests.get(f'http://127.0.0.1:8001/flowers/{flower_id}', headers=headers, timeout=10)
    if response.json() is None:
        raise IncorrectFlowerIDException
    await StarsDAO.add(bouquet_id=flower_id, user_id=current_user['id'])


@stars_router.delete("/{flower_id}")
async def delete_bouquet_from_stars(flower_id: int, current_user = Depends(get_current_user)):
    """Удаление букета из -Избранное-"""
    headers = {'accept': 'application/json'}
    response = requests.get(f'http://127.0.0.1:8001/flowers/{flower_id}', headers=headers, timeout=10)
    if response.json() is None:
        raise IncorrectFlowerIDException
    await StarsDAO.delete(bouquet_id=flower_id, user_id=current_user['id'])
