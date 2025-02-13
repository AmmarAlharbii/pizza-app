from pydantic import BaseModel, Field


class LoginModel(BaseModel):
    username :str = Field('iiMoro', max_length=25)
    password : str 