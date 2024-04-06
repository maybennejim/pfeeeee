from pydantic import BaseModel,Field
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from database import Base



class UserList(BaseModel):
     id    : str
     username : str
     password : str
     password_Crypted : str
     first_name : str
     last_name : str
     create_at : str
     status : str

    
class UserEntry(BaseModel):
    username : str = Field(..., exemple ="potinejj")
    password : str = Field(..., exemple ="potinejj")
    first_name : str = Field(..., exemple ="potine")
    last_name : str = Field(..., exemple ="Sambo")


class UserUpdate(BaseModel):
    id     : str = Field(..., exemple ="Enter your id")
    first_name : str = Field(..., exemple ="Potine")
    last_name : str = Field(..., exemple ="Sambo")
    status  : str = Field (..., exemple ="1")

    
class UserDelete(BaseModel):
    id: str = Field(..., exemple="Enter your id " )


class Loginclass(BaseModel):
    username: str
    password : str

