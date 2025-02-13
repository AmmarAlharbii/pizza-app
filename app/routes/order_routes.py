from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from app.models import Order
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import User
from app.schemas.order_schema import OrderModel, OrderUpdateModel, StatusUpdateModel
from .dependencies import verify_token, update_order_details
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException


order_router = APIRouter(
    prefix='/order', tags=['Order'], dependencies=[Depends(verify_token)])


@order_router.get('/', status_code=status.HTTP_200_OK, response_model=List[OrderModel])
async def get_all_orders(auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    user_orders = session.query(Order).all()
    order_list = []
    for order in user_orders:
        order_list.append({
            "id": order.id,
            'user_id': order.user_id,
            "quantity": order.quantity,
            "order_status": str(order.order_status),
            "pizza_sizes":  str(order.pizza_sizes)
        })
    if user.is_staff:
        return jsonable_encoder(order_list)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid permissions")


@order_router.get('/user', status_code=status.HTTP_200_OK, response_model=List[OrderModel])
async def get_all_orders_by_user(auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    order_list = []
    for order in user.orders:
        order_list.append({
            "id": order.id,
            'user_id': order.user_id,
            "quantity": order.quantity,
            "order_status": str(order.order_status),
            "pizza_sizes":  str(order.pizza_sizes)
        })
    return jsonable_encoder(order_list)


@order_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def get_order_by_id(id: int, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid permissions")
    order = session.query(Order).filter(Order.id == id).first()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
        return {}
    response = OrderModel(id=order.id,
                          user_id=order.user_id,
                          quantity=order.quantity,
                          order_status=str(order.order_status),
                          pizza_sizes=str(order.pizza_sizes))

    return jsonable_encoder(response)

# TODO: enh this function


@order_router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def get_order_by_id_user(id: int, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid permissions")
    orders = user.orders
    for order in orders:
        if order.id == id:
            return jsonable_encoder(OrderModel(id=order.id,
                                               user_id=order.user_id,
                                               quantity=order.quantity,
                                               order_status=str(
                                                   order.order_status),
                                               pizza_sizes=str(order.pizza_sizes)))

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
    )

# get order by id if the user has this order


@order_router.get('/user/order/{id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def get_user_specific_order(id: int, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    orders = user.orders
    for order in orders:
        if order.id == id:
            return jsonable_encoder(OrderModel(id=order.id,
                                               user_id=order.user_id,
                                               quantity=order.quantity,
                                               order_status=str(
                                                   order.order_status),
                                               pizza_sizes=str(order.pizza_sizes)))

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.post("/place-order", status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    # check if the user exists in DB
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(pizza_sizes=order.pizza_sizes, quantity=order.quantity)
    # assign order to user
    new_order.user = user
    session.add(new_order)
    session.commit()
    response = {
        'pizza_sizes': new_order.pizza_sizes,
        'quantity': new_order.quantity,
        'id': new_order.id,
        'order_status': new_order.order_status
    }
    return jsonable_encoder(response)


@order_router.put('/update/{id}', status_code=status.HTTP_200_OK)
async def update_order(id: int, order: OrderUpdateModel, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    # check if user is exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Check if the order belongs to the staff or a regular user
    updated_order = session.query(Order).filter(Order.id == id).first()
    if updated_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Update the order details, using the helper function
    updated_order = update_order_details(updated_order, order)

    # If the user is staff, update the order
    if user.is_staff:
        session.commit()
        response = OrderUpdateModel(
            quantity=updated_order.quantity,     pizza_sizes=str(
                updated_order.pizza_sizes)  # Convert pizza_sizes to string
        )
        return jsonable_encoder(response)

    # check if the order belongs to the user
    if user.orders is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User doesn't have orders")
    # Check if the order belongs to the user
    for each_order in user.orders:
        if each_order.id == updated_order.id:
            updated_order = update_order_details(
                updated_order, order)  # Avoid repeating code
            session.commit()
            response = OrderUpdateModel(
                quantity=updated_order.quantity,     pizza_sizes=str(
                    updated_order.pizza_sizes)  # Convert pizza_sizes to string
            )
            return jsonable_encoder(response)

    # If the order wasn't found among the user's orders
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Order not found")


@order_router.patch('/update/status/{id}', status_code=status.HTTP_200_OK)
async def update_order_status(id: int, order: StatusUpdateModel, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    # check if user is exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   # If the user is staff, update the status

    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid permissions")

        # Check if the order belongs to the staff or a regular user
    updated_order = session.query(Order).filter(Order.id == id).first()
    if updated_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Update the order details, using the helper function
    updated_order.order_status = str(order.order_status)

    session.commit()
    response = {"order_status": updated_order.order_status}

    return jsonable_encoder(response)


@order_router.delete('/delete/{id}')
async def delete_order(id: int, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    current_user = auth.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        session.delete(order)
        session.commit()
        return order
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid permissions")
