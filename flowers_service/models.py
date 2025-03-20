from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from flowers_service.db import Base

class Categories(Base):
    """Модель категории цветов"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class Bouquets(Base):
    """Модель пользователя"""
    __tablename__ = "bouquets"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)


class BouquetComponents(Base):
    """Модель состава букета"""
    __tablename__ = "bouquet_components"
    
    id = Column(Integer, primary_key=True, nullable=False)
    bouquet_id = Column(ForeignKey("bouquets.id"))
    flower_id = Column(ForeignKey("categories.id"))
    quantity = Column(Integer, nullable=False)

