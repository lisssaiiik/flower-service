from sqlalchemy import Column, ForeignKey, Integer
from cart_service.db import Base


class BasketItem(Base):
    __tablename__ = "basket_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bouquet_id = Column(Integer, ForeignKey("bouquets.id"))
    quantity = Column(Integer, default=1, nullable=False)


class Stars(Base):
    """Модель избранного"""
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True)
    bouquet_id = Column(ForeignKey("bouquets.id"))
    user_id = Column(ForeignKey("users.id"))