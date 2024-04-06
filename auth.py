from datetime import timedelta , datetime
from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from User.models import * 
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt , JWTError
import databases,sqlalchemy,datetime,uuid
from Tables import *
from schema import *
from datetime import datetime, timedelta

router = APIRouter (
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
ALGORITHM = "HS256"
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/token",response_model=Token)
async def login_for_acces_token(from_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                                db : db_dependency):
    user = await authenticate_user (from_data.username,from_data.password,db)
    if user:
        token = create_access_token(user['username'], user['password'], user['id'], timedelta(minutes=20))
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


async def authenticate_user(username : str ,password : str ,db):
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if user and user['password'] == password:
        return user
    return None
    
def create_access_token(username : str ,password : str ,user_id : int , expires_delta: timedelta):
    encode={'username': username , 'password':password, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token : Annotated [str,Depends(oauth2_bearer)]):
    try: 
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get('username')
        user_id:str = payload.get('id')
        if username is None or user_id is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail ='could not validate user .')
        return{'username': username ,'id': user_id }
    except JWTError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = 'could not validate user.')
                 
