from pydantic import BaseModel, Field
from typing import Optional


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    user_id: Optional[int]
    order_status: Optional[str] = "PENDING"
    pizza_sizes: Optional[str] = 'SMALL'

    class Config:

        from_attributes = True
        json_schema_extra = {
            'example': {
                'quantity': 1, 'pizza_sizes': "LARGE",

            }
        }


class OrderUpdateModel(BaseModel):
    quantity: int
    # order_status: Optional[str] = "PENDING"
    pizza_sizes: Optional[str] = 'SMALL'

    class Config:

        from_attributes = True
        json_schema_extra = {
            'example': {
                'quantity': 1, 'pizza_sizes': "LARGE",

            }
        }


class StatusUpdateModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:

        from_attributes = True
        json_schema_extra = {
            'example': {
                'quantity': 1, 'pizza_sizes': "LARGE",

            }
        }
