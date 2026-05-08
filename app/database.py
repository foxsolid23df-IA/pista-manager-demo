import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import urllib.parse
import ssl

# 1. Cargar variables del archivo .env
load_dotenv()

# Priorizamos DATABASE_URL (estándar en Render)
# Render proporciona la URL en la variable DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Si no hay DATABASE_URL, intentamos construirla con variables individuales
    SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    USER = os.getenv("POSTGRES_USER", "postgres")
    PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    DB_NAME = os.getenv("POSTGRES_DB", "pista_hielo_db")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}"

# Ajuste para compatibilidad de drivers en Render/SQLAlchemy
# 1. Corregir el prefijo 'postgres://' a 'postgresql://' (común en Heroku/Render)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Forzar pg8000 para evitar dependencias de C y manejar SSL correctamente
if "pg8000" not in SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)

# Depuración (ocultando el password)
debug_url = SQLALCHEMY_DATABASE_URL
if ":" in debug_url and "@" in debug_url:
    parts = debug_url.split("@")
    scheme_user = parts[0].split(":")
    if len(scheme_user) > 2:
        debug_url = f"{scheme_user[0]}:{scheme_user[1]}:****@{parts[1]}"

print(f"INFO: Intentando conectar a: {debug_url}")

# 4. Crear el motor (Engine) con configuraciones robustas para Render
# Configuramos SSL para pg8000
connect_args = {}
if SQLALCHEMY_DATABASE_URL and "localhost" not in SQLALCHEMY_DATABASE_URL:
    # Para pg8000, creamos un contexto SSL
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE # Render usa certificados auto-firmados o de CA interna
    
    connect_args = {
        "ssl_context": ssl_context,
        "timeout": 15
    }

# Usamos pg8000 como driver principal
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
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
