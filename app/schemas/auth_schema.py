from pydantic import BaseModel,Field
from typing import  Optional

class SignUpModel(BaseModel):
    id: int | None = Field(None, exclude=True)  # Use `exclude=True` to mark `id` as excluded in the body
    username :str = Field('iiMoro', max_length=25)
    email :str = Field(max_length=100,pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",default="ammar@gmail.com")
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
    email : str
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