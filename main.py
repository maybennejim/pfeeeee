from http.client import HTTPException
from typing import Annotated, Union
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, MetaData, Table, Column, String, CHAR, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker,Session
from fastapi.encoders import jsonable_encoder
import jwt 
from fastapi.middleware.cors import CORSMiddleware
from typing import List 
import databases,sqlalchemy,datetime,uuid
from passlib.context import CryptContext
from schema import *
from Tables import * 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jwt import PyJWTError
import datetime
from pydantic import ValidationError
import auth 
from fastapi import Depends
from typing import Optional, List
from passlib.hash import bcrypt

pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")


# DATABASE_URL = "postgresql://postgres:admin@localhost:5432/Biat"
# engine = sqlalchemy.create_engine(
#     DATABASE_URL 
# )
# metadata = sqlalchemy.MetaData()
# database = databases.Database(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


origins = [
    "http://localhost",
    "http://localhost:3000",  
]


app = FastAPI()
app.include_router(auth.router)

SECRET_KEY = "BiatLogin"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=800

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/loginUser")

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


# users = Table(
#     "py_users",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("username", String),
#     Column("password", String),
#     Column("password_Crypted", String),
#     Column("first_name", String),
#     Column("last_name", String),
#     Column("create_at", String),
#     Column("status", CHAR),
#     Column("role_id", String, ForeignKey("roles.id"), nullable=True),
#     # Column("agence_id", String, ForeignKey("agence.id", ondelete="CASCADE")),  # Clé étrangère vers Agence

# )

# roles = Table(
#     "roles",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("RoleName", String, unique=True),
# )

# formulaire = Table(
#     "formulaire",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("Agence", String),
#     Column("Societe", String),
#     Column("Type", String),
#     Column("Activite", String),
#     Column("Forme_jur", String),
#     Column("Capital", String),
#     Column("Groupe_dappartenance", String),
#     Column("Adresse", String),
#     Column("Tel", String),
#     Column("Dirigeant", String),
#     Column("Vav", String),
#     Column("Statut", String),
#     Column("Etat", String),
#     Column("Client_conventionee_Biat", Boolean),
#     Column("Conventionne_autre_banque", Boolean),
#     Column("id_condition", ForeignKey("condition.id", ondelete="CASCADE")),
#     Column("id_zone", ForeignKey("zone.id", ondelete="CASCADE")),
    
# )

# Zone = Table(
#     "zone",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("Nom_Zone", String, unique=True),
#     Column("Libelle", String, unique=True,nullable=True),

# )
# Agence = Table(
#     "agence",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("NomAgence", String, unique=True),
#     Column("zone_id", String, ForeignKey("zone.id", ondelete="CASCADE")),  # Clé étrangère vers Zone
#     Column("Id_charge_client", String, ForeignKey("py_users.id", ondelete="CASCADE")),
#     Column("Id_responsable", String, ForeignKey("py_users.id", ondelete="CASCADE")),
#     Column("Id_directeur_groupe", String, ForeignKey("py_users.id", ondelete="CASCADE")),
#     Column("Id_directeur_region", String, ForeignKey("py_users.id", ondelete="CASCADE")),
# )
# Avis = Table(
#     "avis",
#     metadata,
#     Column("id",String, primary_key=True, index=True),
#     Column("Duree", Integer ),
#     Column("Taux", Float ),
#     Column("Nature", String ),
#     Column("Famille",ForeignKey("famille.id", ondelete="CASCADE")),
# )
# Condition = Table (
#     "condition",
#     metadata ,
#     Column("id", String, primary_key=True),
#     Column("Taux", Float ),
#     Column("Cmp", Integer ),
#     Column("Commentaire", String ),
#     Column("id_zone",ForeignKey("zone.id", ondelete="CASCADE")),
# )
    
# Famille = Table (
#     "famille",
#     metadata ,
#     Column("id", String, primary_key=True),
#     Column("designation", String),
#     )

# Nature = Table (
#     "nature",
#     metadata ,
#     Column("id", String, primary_key=True),
#     Column("nom", String),
#     Column("taux", Float),
#     Column("duree", Integer ),
#     Column("id_famille",ForeignKey("famille.id", ondelete="CASCADE")),
# )

# metadata.create_all(engine)




@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "msg": "Validation Error"},
    )

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/",status_code=status.HTTP_200_OK)
async def user(user:None, db:db_dependency): # type: ignore
    if user is None:
        raise HTTPException(status_code=401,detail='Authentification Failed')
    return {"User":user}


@app.get("/items/{item_id}")
def read_item (item_id:int , q:Union [str, None]=None):
    return {"item_id":item_id,"q":q}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def authenticate_user(username: str, password: str):
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if user and user['password'] == password:
        return user
    return None

@app.post("/loginUser")
async def login_user(login_item: Loginclass):
    user = await authenticate_user(login_item.username, login_item.password)
    if user:
        token = create_access_token(user.username, user.id, timedelta(minutes=20))
        
        return {'status': '200', 'token': token}
    else:
        raise HTTPException(status_code=401, detail="Login failed")


@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route"}

async def get_current_active_user(current_user: str = Depends(auth.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_is_active = True 
    if not user_is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

@app.get("/users",response_model=list[UserList])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.post("/Create_role",response_model = RoleList)
async def register_role (role : RoleEntry,  current_user: str = Depends(get_current_active_user)):
    idRole = str(uuid.uuid1())
    query = roles.insert().values(
    id = idRole,
    RoleName = role.RoleName
    )
    await database.execute(query)
    return {"id": idRole}

@app.get("/listRole", response_model=list[RoleList])
async def find_all_roles():
    query = roles.select()
    return await database.fetch_all(query)


@app.put("/role_update", response_model=RoleUpdateEntry)
async def update_role(role : RoleUpdateEntry):
    query = roles.update().\
         where(roles.c.id == role.id).\
         values(
             RoleName =role.RoleName,
         )
    await database.execute(query)
    return {
        "status": True,
        "message":"this role has been modified succesfully."
    }

@app.delete("/Delete_Role/{roleId}")
async def delete_Role(user:RoleDelete):
    query = roles.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status": True,
        "message":"this user has bbeen deleted succesfully."
    }


@app.post("/users")
async def regsister_user(user: UserEntry):
    try:
        gid = str(uuid.uuid1())
        gDate = str(datetime.datetime.now())
        query = users.insert().values(
            id=gid,
            username=user.username,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            create_at=gDate,
            status="1",
            password_Crypted=pwd_context.hash(user.password)
        )
        await database.execute(query)
        return {"status": 200}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/{userId}", response_model=UserList)
async def find_user_by_id(userId: str):
    query = users.select().where(users.c.id == userId)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/username/{userName}", response_model=UserList)
async def find_user_by_username(username: str):
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users", response_model=UserList)
async def update_user(user : UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
         where(users.c.id == user.id).\
         values(
             first_name =user.first_name,
             last_name = user.last_name,
             create_at = gDate,
         )
    await database.execute(query)
    return await find_user_by_id(user.id)

@app.delete("/users/{userId}")
async def delete_user(user:UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)
    return {
        "status": True,
        "message":"this user has bbeen deleted succesfully."
    }


@app.post("/users")
async def regsister_user(user: UserEntry, db:Session = Depends(get_db)):
    gid = str(uuid.uuid1())
    gDate=str(datetime.datetime.now())
    query =users.insert().values(
        id = gid,
        username = user.username,
        password = user.password,
        first_name =user.first_name,
        last_name = user.last_name,
        create_at = gDate,
        status = "1",
        password_Crypted =pwd_context.hash(user.password)
    )
    db.add(query)
    db.commit()
    return 
    {
        "Message":"Created"
    }

class FormulaireCreate(BaseModel):
    Agence: str
    Societe: str
    Type: str
    Activite: Optional[str] = None
    Forme_jur: Optional[str] = None
    Capital: Optional[str] = None
    Groupe_dappartenance: Optional[str] = None
    Adresse: Optional[str] = None
    Tel: Optional[str] = None
    Dirigeant: Optional[str] = None
    Vav: Optional[str] = None
    Statut: Optional[str] = None
    Etat: Optional[str] = None
    Client_conventionee_Biat: Optional[bool] = None
    Conventionne_autre_banque: Optional[bool] = None
    id_zone: Optional[str] = None

class FormulaireList(BaseModel):
    id: str
    Agence: str
    Societe: str
    Type: str
    Activite: Optional[str] = None
    Forme_jur: Optional[str] = None
    Capital: Optional[str] = None
    Groupe_dappartenance: Optional[str] = None
    Adresse: Optional[str] = None
    Tel: Optional[str] = None
    Dirigeant: Optional[str] = None
    Vav: Optional[str] = None
    Statut: Optional[str] = None
    Etat: Optional[str] = None
    Client_conventionee_Biat: Optional[bool] = None
    Conventionne_autre_banque: Optional[bool] = None
    id_zone: Optional[str] = None

Session = sessionmaker(bind=engine)

def create_formulaire(formulaire_data: FormulaireCreate):
    with Session() as session:
        formulaire_id = str(uuid.uuid1())  # Generate a UUID for the formulaire
        formulaire_data_dict = formulaire_data.dict()
        formulaire_data_dict["id"] = formulaire_id  # Assign the generated UUID to the 'id' field
        new_formulaire = formulaire.insert().values(**formulaire_data_dict)
        session.execute(new_formulaire)
        session.commit()
        return new_formulaire

def get_formulaire(id: str):
    with Session() as session:
        stmt = formulaire.select().where(formulaire.c.id == id)
        return session.execute(stmt).fetchone()

def list_formulaire():
    with Session() as session:
        stmt = formulaire.select()
        return session.execute(stmt).fetchall()

@app.post("/formulaire/", response_model=FormulaireList)
def create_new_formulaire(formulaire_data: FormulaireCreate):
    return create_formulaire(formulaire_data)

@app.get("/formulaire/{id}", response_model=FormulaireList)
def read_formulaire(id: str):
    formulaire_data = get_formulaire(id)
    if formulaire_data is None:
        raise HTTPException(status_code=404, detail="Formulaire not found")
    return formulaire_data

@app.get("/formulaire/", response_model=List[FormulaireList])
def list_formulaire_api():
    return list_formulaire()


class ZoneCreate(BaseModel):
    Nom_Zone: str
    Libelle: str = None

class ZoneList(BaseModel):
    id: str
    Nom_Zone: str
    Libelle: str = None
from Tables import Zone
def create_zone(zone_data: ZoneCreate):
    with Session() as session:
        zone_id = str(uuid.uuid1())  # Generate a UUID for the zone
        zone_data_dict = zone_data.dict()
        zone_data_dict["id"] = zone_id  # Assign the generated UUID to the 'id' field
        new_zone = Zone.insert().values(**zone_data_dict)
        session.execute(new_zone)
        session.commit()
        return new_zone

def list_zones():
    with Session() as session:
        stmt = Zone.select()
        return session.execute(stmt).fetchall()

# API routes
@app.post("/zones/", response_model=ZoneList)
def create_new_zone(zone_data: ZoneCreate):
    return create_zone(zone_data)

@app.get("/zones/", response_model=list[ZoneList])
def list_zones_api():
    return list_zones()


from Tables import Agence
class AgenceCreate(BaseModel):
    NomAgence: str
    zone_id: str
    Id_charge_client: str
    Id_responsable: str
    Id_directeur_groupe: str
    Id_directeur_region: str

class AgenceList(BaseModel):
    id: str
    NomAgence: str
    zone_id: str
    Id_charge_client: str
    Id_responsable: str
    Id_directeur_groupe: str
    Id_directeur_region: str

Session = sessionmaker(bind=engine)

def create_agence(agence_data: AgenceCreate):
    with Session() as session:
        agence_id = str(uuid.uuid1())  # Generate a UUID for the agence
        agence_data_dict = agence_data.dict()
        agence_data_dict["id"] = agence_id  # Assign the generated UUID to the 'id' field
        new_agence = Agence.insert().values(**agence_data_dict)
        session.execute(new_agence)
        session.commit()
        return new_agence

def list_agences():
    with Session() as session:
        stmt = Agence.select()
        return session.execute(stmt).fetchall()

@app.post("/agences/", response_model=AgenceList)
def create_new_agence(agence_data: AgenceCreate):
    return create_agence(agence_data)

@app.get("/agences/", response_model=list[AgenceList])
def list_agences_api():
    return list_agences()


class AvisCreate(BaseModel):
    Duree: int
    Taux: float
    Nature: str
    Famille: str

# Pydantic model for listing avis
class AvisList(BaseModel):
    id: str
    Duree: int
    Taux: float
    Nature: str
    Famille: str


def create_avis(avis_data: AvisCreate):
    with Session() as session:
        avis_id = str(uuid.uuid1())  # Generate a UUID for the avis
        avis_data_dict = avis_data.dict()
        avis_data_dict["id"] = avis_id  # Assign the generated UUID to the 'id' field
        new_avis = Avis.insert().values(**avis_data_dict)
        session.execute(new_avis)
        session.commit()
        return new_avis

def list_avis():
    with Session() as session:
        stmt = Avis.select()
        return session.execute(stmt).fetchall()

# API routes
@app.post("/avis/", response_model=AvisList)
def create_new_avis(avis_data: AvisCreate):
    return create_avis(avis_data)

@app.get("/avis/", response_model=list[AvisList])
def list_avis_api():
    return list_avis()


class ConditionCreate(BaseModel):
    Taux: float
    Cmp: int
    Commentaire: str
    id_zone: str

# Pydantic model for listing condition
class ConditionList(BaseModel):
    id: str
    Taux: float
    Cmp: int
    Commentaire: str
    id_zone: str

def create_condition(condition_data: ConditionCreate):
    with Session() as session:
        condition_id = str(uuid.uuid1())  # Generate a UUID for the condition
        condition_data_dict = condition_data.dict()
        condition_data_dict["id"] = condition_id  # Assign the generated UUID to the 'id' field
        new_condition = Condition.insert().values(**condition_data_dict)
        session.execute(new_condition)
        session.commit()
        return new_condition

def list_conditions():
    with Session() as session:
        stmt = Condition.select()
        return session.execute(stmt).fetchall()

@app.post("/conditions/", response_model=ConditionList)
def create_new_condition(condition_data: ConditionCreate):
    return create_condition(condition_data)

@app.get("/conditions/", response_model=list[ConditionList])
def list_conditions_api():
    return list_conditions()

class FamilleCreate(BaseModel):
    designation: str

# Pydantic model for listing famille
class FamilleList(BaseModel):
    id: str
    designation: str

def create_famille(famille_data: FamilleCreate):
    with Session() as session:
        famille_id = str(uuid.uuid1())  # Generate a UUID for the famille
        famille_data_dict = famille_data.dict()
        famille_data_dict["id"] = famille_id  # Assign the generated UUID to the 'id' field
        new_famille = Famille.insert().values(**famille_data_dict)
        session.execute(new_famille)
        session.commit()
        return new_famille

def list_familles():
    with Session() as session:
        stmt = Famille.select()
        return session.execute(stmt).fetchall()

# API routes
@app.post("/familles/", response_model=FamilleList)
def create_new_famille(famille_data: FamilleCreate):
    return create_famille(famille_data)

@app.get("/familles/", response_model=list[FamilleList])
def list_familles_api():
    return list_familles()


class NatureCreate(BaseModel):
    nom: str
    taux: float
    duree: int
    id_famille: str

# Pydantic model for listing nature
class NatureList(BaseModel):
    id: str
    nom: str
    taux: float
    duree: int
    id_famille: str


def create_nature(nature_data: NatureCreate):
    with Session() as session:
        nature_id = str(uuid.uuid1())  # Generate a UUID for the nature
        nature_data_dict = nature_data.dict()
        nature_data_dict["id"] = nature_id  # Assign the generated UUID to the 'id' field
        new_nature = Nature.insert().values(**nature_data_dict)
        session.execute(new_nature)
        session.commit()
        return new_nature

def list_natures():
    with Session() as session:
        stmt = Nature.select()
        return session.execute(stmt).fetchall()

@app.post("/natures/", response_model=NatureList)
def create_new_nature(nature_data: NatureCreate):
    return create_nature(nature_data)

@app.get("/natures/", response_model=list[NatureList])
def list_natures_api():
    return list_natures()