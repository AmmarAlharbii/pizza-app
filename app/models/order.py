from app.database.db import Base
from sqlalchemy import Column, Integer, Text, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
# from app.models.user import User


class Order(Base):
    ORDER_STATUSES = (
        ("PENDING", 'pending'),
        ("IN-TRANSIT", 'in-transit'),
        ("DELIVERED", 'delivered'),
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large'),
    )

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    order_status = Column(ChoiceType(
        choices=ORDER_STATUSES, impl=String()), default='PENDING')
    pizza_sizes = Column(ChoiceType(choices=PIZZA_SIZES,
                         impl=String()), default='SMALL')
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.user_id}>"
