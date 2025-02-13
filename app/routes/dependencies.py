from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT

from app.models.order import Order
from app.schemas.order_schema import OrderUpdateModel, StatusUpdateModel


def verify_token(auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )


def update_order_details(updated_order: Order, order: OrderUpdateModel):
    updated_order.quantity = order.quantity
    updated_order.pizza_sizes = order.pizza_sizes if order.pizza_sizes else updated_order.pizza_sizes
    return updated_order
