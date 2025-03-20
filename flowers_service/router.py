from typing import List, Optional
from fastapi import Depends, Query
from fastapi import APIRouter
from flowers_service.dao import BouquetsDAO, CategoriesDAO, ComponentsDAO
from flowers_service.dependencies import get_current_user
from flowers_service.exceptions import IncorrectFlowerIDException, IncorrectRoleException
from flowers_service.schemas import SAddBouquet, SBouquetsInfo, SComponentBouquet


router = APIRouter(prefix="/flowers", tags=["Цвяточки"])


@router.get("/filters/")
async def get_bouquets_by_filters(
    min_price: Optional[int] = Query(description="Минимальная цена букета",default=0),
    max_price: Optional[int] = Query(description="Максимальная цена букета", default=1_000_000),
    flowers_in_bouquet: Optional[List[str]] = Query(None, description="Цветы, входящие в составь букета, вводите через запятую")):
    """Возвращает все букеты"""
    if flowers_in_bouquet is not None:
        flowers_in_bouquet = flowers_in_bouquet[0].split(",")
    bouquets = await BouquetsDAO.find_all_by_filters(min_price, max_price, flowers_in_bouquet)
    return bouquets


@router.get("/", response_model=List[SBouquetsInfo])
async def get_bouquets():
    """Возвращает все букеты"""
    bouquets = await BouquetsDAO.find_all()
    return bouquets


@router.get("/{f_id}")
async def get_bouquet(f_id: int):
    """Возвращает букет по ID"""
    bouquet = await BouquetsDAO.find_by_id(f_id)
    return bouquet


@router.post("/")
async def add_bouquet(add_flower: SAddBouquet,
                      components: List[SComponentBouquet],
                      current_user = Depends(get_current_user)):
    """Добавление цветов в каталог товаров. Доступно только администраторам"""
    if current_user['role'] != 'admin':
        raise IncorrectRoleException
    if components == []: # проверка, что список не пустой
        raise IncorrectFlowerIDException
    # добавляем букет в БД
    buq_id = await BouquetsDAO.add(name=add_flower.name,
                                     description=add_flower.description,
                                     price=add_flower.price,
                                     stock_quantity=add_flower.stock_quantity)
    # добавляем компоненты букета в БД
    for component in components:
        await ComponentsDAO.add(bouquet_id=buq_id,
                                flower_id=component.flower_id,
                                quantity=component.quantity)
    return {"status": "success",
            "detail": f"Был добавлен букет с ID {buq_id}"}


@router.post("/category")
async def add_category(category: str, current_user = Depends(get_current_user)):
    """Добавление категории цветов. Доступно только администраторам"""
    if current_user['role'] != 'admin':
        raise IncorrectRoleException
    await CategoriesDAO.add(name=category)


@router.put("/description/{bouquet_id}")
async def update_bouquets(bouquet_id: int, new_description: str, current_user = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise IncorrectRoleException
    bouquet = await BouquetsDAO.find_by_id(model_id=bouquet_id)
    if bouquet is None:
        raise IncorrectFlowerIDException
    await BouquetsDAO.update(flower_id=bouquet_id, description=new_description)
