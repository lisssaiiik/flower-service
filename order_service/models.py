from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from order_service.db import Base

class Order(Base):
    """Модель заказа"""
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey("users.id"))
    order_date = Column(Date)
    total_cost = Column(Float)
    order_status = Column(String, nullable=False)
    payment_method = Column(String)
    shipping_method = Column(String)
    is_delivered = Column(Boolean)
    address = Column(String)
