from pydantic import BaseModel

class SBouquetsInfo(BaseModel):
    """Схема инфы о цветочке"""
    id: int
    name: str
    description: str 
    price: float
    stock_quantity: int 

class SAddBouquet(BaseModel):
    """Схема добавления букета"""
    name: str
    description: str
    price: float
    stock_quantity: int


class SComponentBouquet(BaseModel):
    """Компонент букета"""
    flower_id: int
    quantity: int

