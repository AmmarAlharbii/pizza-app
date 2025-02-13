# app/models/__init__.py
from .user import User
from .order import Order

# This ensures both models are imported when someone imports from models
__all__ = ["User", "Order"]