from pydantic import BaseModel,Field,EmailStr
from typing import  Optional

class SignUpModel(BaseModel):
    id: int | None = Field(None, exclude=True)  # Use `exclude=True` to mark `id` as excluded in the body
    username :str = Field('iiMoro', max_length=25)
    email: EmailStr
    password : str 
    is_staff: Optional [bool] = False
    is_active : Optional [bool]
    
    
    class Config: 
        from_attributes = True
        json_schema_extra = {
            'example':{
                'username':'Ammar'
                ,'email':"Ammar@gmail.com"
                ,"password":'password',
                'is_staff':False,
                'is_active':True
            }
        }
        
class SignUpResponse(BaseModel):
    username :str
    email: EmailStr
    is_staff: Optional [bool]
    is_active : Optional [bool]        
    class Config: 
        from_attributes = True
        json_schema_extra = {
            'example':{
                'username':'Ammar'
                ,'email':"Ammar@gmail.com",
                'is_staff':False,
                'is_active':True
            }
        }