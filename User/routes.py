# from User.models import *
# from http.client import HTTPException
# from fastapi import APIRouter, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# import jwt 
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from datetime import datetime, timedelta
# from jwt import PyJWTError
# from pydantic import ValidationError
# from Tables import users
# from config import *
# import database,sqlalchemy,datetime,uuid



# user_route = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/loginUser")

# @user_route.exception_handler(ValidationError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=422,
#         content={"detail": exc.errors(), "msg": "Validation Error"},
#     )

# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except PyJWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return username


# async def authenticate_user(username: str, password: str):
#     query = users.select().where(users.c.username == username)
#     user = await database.fetch_one(query)
#     if user and user['password'] == password:
#         return user
#     return None

# @user_route.post("/loginUser")
# async def login_user(login_item: Loginclass):
#     user = await authenticate_user(login_item.username, login_item.password)
#     if user:
#         encoded_jwt = jwt.encode({"sub": user['username']}, SECRET_KEY, algorithm=ALGORITHM)
#         return {'status': '200', 'token': encoded_jwt}
#     else:
#         raise HTTPException(status_code=401, detail="Login failed")

# @user_route.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     return {"message": "This is a protected route"}

# async def get_current_active_user(current_user: str = Depends(get_current_user)):
#     user = find_user_by_username(current_user)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     if not user.is_active:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
#     return user

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except PyJWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return username

# @user_route.get("/users",response_model=list[UserList])
# async def find_all_users():
#     query = users.select()
#     return await database.fetch_all(query)


# @user_route.post("/users", response_model =UserList)
# async def regsister_user(user: UserEntry):
#     gid = str(uuid.uuid1())
#     gDate=str(datetime.datetime.now())
#     query =users.insert().values(
#         id = gid,
#         username = user.username,
#         password = user.password,
#         first_name =user.first_name,
#         last_name = user.last_name,
#         create_at = gDate,
#         status = "1",
#         password_Crypted =pwd_context.hash(user.password)
#     )
#     await database.execute(query)
#     return {
#         "id" : gid,
#         **user.dict(),
#         "create_at" : gDate,
#         "status":"1"
#     }

# @user_route.get("/users/{userId}", response_model=UserList)
# async def find_user_by_id(userId: str):
#     query = users.select().where(users.c.id == userId)
#     user = await database.fetch_one(query)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @user_route.get("/username/{userName}", response_model=UserList)
# async def find_user_by_username(username: str):
#     query = users.select().where(users.c.username == username)
#     user = await database.fetch_one(query)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @user_route.put("/users", response_model=UserList)
# async def update_user(user : UserUpdate):
#     gDate = str(datetime.datetime.now())
#     query = users.update().\
#          where(users.c.id == user.id).\
#          values(
#              first_name =user.first_name,
#              last_name = user.last_name,
#              create_at = gDate,
#          )
#     await database.execute(query)

#     return await find_user_by_id(user.id)

# @user_route.delete("/users/{userId}")
# async def delete_user(user:UserDelete):
#     query = users.delete().where(users.c.id == user.id)
#     await database.execute(query)

#     return {
#         "status": True,
#         "message":"this user has bbeen deleted succesfully."
#     }

