from typing import List
from pydantic import BaseModel, Field 


class SCart(BaseModel):
    """Корзина"""
    id: int


class SOrder(BaseModel):
    """Создание заказа"""
    cart: List[SCart]
    shipping_method: str = Field(default="самовывоз", description="курьер cамовывоз")
    address: str = Field(default="адрес магазина для самовывоза")