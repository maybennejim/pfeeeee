from sqlalchemy import create_engine, MetaData, Table, Column, String, CHAR, ForeignKey,Float, Boolean,Integer
import sqlalchemy,databases
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:admin@localhost:5432/Biat"
engine = sqlalchemy.create_engine(
    DATABASE_URL 
)
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

users = Table(
    "py_users",
    metadata,
    Column("id", String, primary_key=True),
    Column("username", String),
    Column("password", String),
    Column("password_Crypted", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("create_at", String),
    Column("status", CHAR),
    Column("role_id", String, ForeignKey("roles.id"), nullable=True),
    # Column("agence_id", String, ForeignKey("agence.id", ondelete="CASCADE")),  # Clé étrangère vers Agence

)

roles = Table(
    "roles",
    metadata,
    Column("id", String, primary_key=True),
    Column("RoleName", String, unique=True),
)

formulaire = Table(
    "formulaire",
    metadata,
    Column("id", String, primary_key=True),
    Column("Agence", String),
    Column("Societe", String),
    Column("Type", String),
    Column("Activite", String),
    Column("Forme_jur", String),
    Column("Capital", String),
    Column("Groupe_dappartenance", String),
    Column("Adresse", String),
    Column("Tel", String),
    Column("Dirigeant", String),
    Column("Vav", String),
    Column("Statut", String),
    Column("Etat", String),
    Column("Client_conventionee_Biat", Boolean),
    Column("Conventionne_autre_banque", Boolean),
    Column("id_zone", ForeignKey("zone.id", ondelete="CASCADE"),nullable=True),
    
)

Zone = Table(
    "zone",
    metadata,
    Column("id", String, primary_key=True),
    Column("Nom_Zone", String, unique=True),
    Column("Libelle", String, unique=True,nullable=True),

)
Agence = Table(
    "agence",
    metadata,
    Column("id", String, primary_key=True),
    Column("NomAgence", String, unique=True),
    Column("zone_id", String, ForeignKey("zone.id", ondelete="CASCADE")),  # Clé étrangère vers Zone
    Column("Id_charge_client", String, ForeignKey("py_users.id", ondelete="CASCADE")),
    Column("Id_responsable", String, ForeignKey("py_users.id", ondelete="CASCADE")),
    Column("Id_directeur_groupe", String, ForeignKey("py_users.id", ondelete="CASCADE")),
    Column("Id_directeur_region", String, ForeignKey("py_users.id", ondelete="CASCADE")),
)
Avis = Table(
    "avis",
    metadata,
    Column("id",String, primary_key=True, index=True),
    Column("Duree", Integer ),
    Column("Taux", Float ),
    Column("Nature", String ),
    Column("Famille",ForeignKey("famille.id", ondelete="CASCADE")),
)
Condition = Table (
    "condition",
    metadata ,
    Column("id", String, primary_key=True),
    Column("Taux", Float ),
    Column("Cmp", Integer ),
    Column("Commentaire", String ),
    Column("id_zone",ForeignKey("zone.id", ondelete="CASCADE")),
)
    
Famille = Table (
    "famille",
    metadata ,
    Column("id", String, primary_key=True),
    Column("designation", String),
    )

Nature = Table (
    "nature",
    metadata ,
    Column("id", String, primary_key=True),
    Column("nom", String),
    Column("taux", Float),
    Column("duree", Integer ),
    Column("id_famille",ForeignKey("famille.id", ondelete="CASCADE")),
)



metadata.create_all(engine)
