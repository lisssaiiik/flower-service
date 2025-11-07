from sqlalchemy import and_, select, insert, update
from db import async_session_maker
from models import BouquetComponents, Bouquets, Categories

class BouquetsDAO:

    model = Bouquets

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
            await session.commit() 
            new_id = res.scalar()  
            return new_id 
        
    @classmethod
    async def update(cls, flower_id, **data):
        """
        Обновляет запись
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == flower_id).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def find_all(cls, **filter_by):
        '''
        Находит все записи в БД, соответствующие условиям
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(
                **filter_by)  
            result = await session.execute(query)
            return result.scalars().all() 


    @classmethod
    async def find_all_by_filters(cls, min_check, max_check, flowers_in_bouquet):
        '''
        Находит все записи в БД, соответствующие условиям
        '''
        

        async with async_session_maker() as session:
            if flowers_in_bouquet is not None:
                query = (select(cls.model,
                            Categories.name)
                            .join(BouquetComponents, cls.model.id == BouquetComponents.bouquet_id)
                            .join(Categories, BouquetComponents.flower_id == Categories.id)
                            .where(and_(Categories.name.in_(flowers_in_bouquet),
                                        cls.model.price >= min_check,
                                        cls.model.price <= max_check)))

            else:
                query = select(cls.model).where(and_(cls.model.price >= min_check,
                                        cls.model.price <= max_check))
            result = await session.execute(query)
            return result.scalars().all()



class CategoriesDAO:

    model = Categories

    @classmethod
    async def add(cls, **data):
        '''
        Добавляет запись в БД
        '''
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            res = await session.execute(query)
            await session.commit()  
            new_id = res.scalar()  
            return new_id 


class ComponentsDAO:

    model = BouquetComponents

    @classmethod
    async def add(cls, **data):
        '''
        Добавляет запись в БД
        '''
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            res = await session.execute(query)
            await session.commit()  
            new_id = res.scalar()  
            return new_id 

