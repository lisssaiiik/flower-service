from typing import List, Optional
from fastapi import APIRouter, Query, Body
from dao import BouquetsDAO, CategoriesDAO, ComponentsDAO
from exceptions import (
    IncorrectFlowerIDException, FlowersException,
    InvalidPriceException, InvalidQuantityException, EmptyFieldException
)
from schemas import (
    SAddBouquetWithComponents, SAddCategory, SUpdateDescription,
    SBouquetsInfo
)

router = APIRouter(prefix="/flowers", tags=["Цвяточки"])

# --- Получение всех букетов по фильтру ---
@router.get("/filters/", response_model=List[SBouquetsInfo])
async def get_bouquets_by_filters(
    min_price: Optional[int] = Query(0, description="Минимальная цена букета"),
    max_price: Optional[int] = Query(1_000_000, description="Максимальная цена букета"),
    flowers_in_bouquet: Optional[List[str]] = Query(None, description="Цветы через запятую")
):
    if min_price < 0 or max_price < 0:
        raise InvalidPriceException(detail="Цены не могут быть отрицательными")
    if min_price > max_price:
        raise InvalidPriceException(detail="Минимальная цена не может быть больше максимальной")
    if flowers_in_bouquet:
        flowers_in_bouquet = flowers_in_bouquet[0].split(",")
    bouquets = await BouquetsDAO.find_all_by_filters(min_price, max_price, flowers_in_bouquet)
    return bouquets

# --- Получение всех букетов ---
@router.get("/", response_model=List[SBouquetsInfo])
async def get_bouquets():
    bouquets = await BouquetsDAO.find_all()
    return bouquets

# --- Получение одного букета по ID ---
@router.get("/{f_id}", response_model=SBouquetsInfo)
async def get_bouquet(f_id: int):
    bouquet = await BouquetsDAO.find_by_id(f_id)
    if not bouquet:
        raise IncorrectFlowerIDException()
    return bouquet

# --- Добавление букета с компонентами ---
@router.post("/", response_model=dict)
async def add_bouquet(body: SAddBouquetWithComponents):
    add_flower = body.add_flower
    components = body.components

    if not add_flower.name.strip() or not add_flower.description.strip():
        raise EmptyFieldException(detail="Название и описание букета не могут быть пустыми")
    if add_flower.price <= 0:
        raise InvalidPriceException(detail="Цена должна быть больше 0")
    if add_flower.stock_quantity < 0:
        raise InvalidQuantityException(detail="Количество не может быть отрицательным")
    if not components:
        raise IncorrectFlowerIDException()

    buq_id = await BouquetsDAO.add(
        name=add_flower.name,
        description=add_flower.description,
        price=add_flower.price,
        stock_quantity=add_flower.stock_quantity
    )

    for component in components:
        if component.quantity <= 0:
            raise InvalidQuantityException(detail="Количество компонента должно быть больше 0")
        await ComponentsDAO.add(
            bouquet_id=buq_id,
            flower_id=component.flower_id,
            quantity=component.quantity
        )
    return {"status": "success", "detail": f"Букет с ID {buq_id} добавлен"}

# --- Добавление категории ---
@router.post("/category", response_model=dict)
async def add_category(body: SAddCategory):
    if not body.category.strip():
        raise EmptyFieldException(detail="Название категории не может быть пустым")
    await CategoriesDAO.add(name=body.category)
    return {"status": "success", "detail": f"Категория '{body.category}' добавлена"}

# --- Обновление описания ---
@router.put("/description/{bouquet_id}", response_model=dict)
async def update_bouquets(bouquet_id: int, body: SUpdateDescription):
    bouquet = await BouquetsDAO.find_by_id(model_id=bouquet_id)
    if not bouquet:
        raise IncorrectFlowerIDException()
    if not body.new_description.strip():
        raise EmptyFieldException(detail="Описание не может быть пустым")

    await BouquetsDAO.update(flower_id=bouquet_id, description=body.new_description)
    return {"status": "success", "detail": f"Описание букета {bouquet_id} обновлено"}
