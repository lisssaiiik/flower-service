from sqlalchemy import delete, select, insert, update
from order_service.models import Order
from users_service.db import async_session_maker


class OrderDAO:

    model = Order

    @classmethod
    async def find_by_id(cls, model_id: int):
        '''
        Находит одну запись в БД по номеру id
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        '''
        Находит одну запись в БД c условиями
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def add(cls, **data):
        '''
        Добавляет запись в БД
        '''
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            res = await session.execute(query)
            await session.commit()  # фиксирует изменения в БД, обязательно
            new_id = res.scalar()  # Получаем id новой записи
            return new_id  # Возвращаем id
        
    @classmethod
    async def update(cls, order_id: int, user_id, **data):
        """
        Обновляет запись

        -Аргументы:
            id: ID записи, которую надо обновить
            **data: атрибуты модели в качестве ключей и их значения в качестве значений.
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == order_id, cls.model.user_id == user_id).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        '''
        Удаляет запись из БД
        '''
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_all(cls, **filter_by):
        '''
        Находит все записи в БД, соответствующие условиям
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(
                **filter_by)  # select * from bookigs
            result = await session.execute(query)
            return result.scalars().all()  # result.mappings().all()