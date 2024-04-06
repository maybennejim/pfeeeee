from pydantic import BaseModel,Field


class UserList(BaseModel):
     id    : str
     username : str
     password : str
     password_Crypted : str
     first_name : str
     last_name : str
     create_at : str
     status : str

class FormulaireList(BaseModel):
    id:str
    Agence:str
    Societe:str
    Type:str
    Activite:str
    Forme_jur:str
    Capital:str
    Groupe_dappartenance:str
    Adresse:str
    Tel:str
    Dirigeant:str
    Vav: str
    Statut:str
    Etat:str
    lient_conventionee_Biat:bool
    Conventionne_autre_banque:bool
    Id_zone:str
    id_condition:str

class FormulaireEntry(BaseModel):
    Agence:str
    Societe:str
    Type:str
    Activite:str
    Forme_jur:str
    Capital:str
    Groupe_dappartenance:str
    Adresse:str
    Tel:str
    Dirigeant:str
    Vav: str
    Statut:str
    Etat:str
    lient_conventionee_Biat:bool
    Conventionne_autre_banque:bool
    Id_zone:str
    id_condition:str



class RoleList(BaseModel):
    id    : str
    RoleName : str = Field(..., exemple ="potinejj")


class RoleEntry(BaseModel):
    RoleName : str = Field(..., exemple ="potinejj")


class RoleUpdateEntry(BaseModel):
    id    : str
    RoleName : str = Field(..., exemple ="potinejj")

class RoleDelete(BaseModel):
    id    : str


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


