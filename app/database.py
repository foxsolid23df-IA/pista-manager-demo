import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Cargar variables del archivo .env
load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
SERVER = os.getenv("POSTGRES_SERVER")
PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# 2. Crear la URL de conexión (Connection String)
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}"

# 3. Crear el motor (Engine)
# pool_pre_ping=True ayuda a reconectar si la BD se cae momentáneamente
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

# 4. Crear la fábrica de sesiones (SessionLocal)
# Cada petición de un usuario usará una sesión propia
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base para los modelos (lo usaremos mañana)
Base = declarative_base()

# 6. Dependencia para FastAPI (Utility function)
# Esto se usa para abrir y CERRAR la conexión automáticamente en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
