from pydantic import BaseModel
from typing import Optional, List

class SBouquetsInfo(BaseModel):
    """Схема информации о букете"""
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

class SAddBouquetWithComponents(BaseModel):
    add_flower: SAddBouquet
    components: List[SComponentBouquet]

class SAddCategory(BaseModel):
    category: str

class SUpdateDescription(BaseModel):
    new_description: str

class SFilterBouquets(BaseModel):
    min_price: Optional[int] = 0
    max_price: Optional[int] = 1_000_000
    flowers_in_bouquet: Optional[List[str]] = None