from sqlalchemy import Column, Date, Integer, String
from users_service.db import Base


class Users(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    phone_number = Column(String, unique=True)
    date_of_birth = Column(Date)
    address = Column(String)
    hashed_password = Column(String)
    role = Column(String, nullable=True, default='user')
