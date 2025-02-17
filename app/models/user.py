from app.database.db import Base
from sqlalchemy import Column, Integer, Text, Boolean, String
from sqlalchemy.orm import relationship
# models.py
from sqlalchemy.ext.declarative import declarative_base
# from app.models.order import Order  # Only for type hints


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(100), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
