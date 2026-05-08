import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Cargar variables del archivo .env
load_dotenv()

# Priorizamos DATABASE_URL (estándar en Render)
# Si es una URL de ejemplo (contiene 'hostname' o 'port'), la ignoramos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URL and ("hostname" in SQLALCHEMY_DATABASE_URL or "port" in SQLALCHEMY_DATABASE_URL):
    SQLALCHEMY_DATABASE_URL = None

if not SQLALCHEMY_DATABASE_URL:
    # Si no hay DATABASE_URL, construimos una con las variables individuales
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    SERVER = os.getenv("POSTGRES_SERVER")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    
    # Aseguramos que el puerto sea un número, si no, usamos el default
    if not PORT or not PORT.isdigit():
        PORT = "5432"
        
    DB_NAME = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}"

# 2. Corrección de protocolo y dialecto
# SQLAlchemy 2.0 prefiere 'postgresql+psycopg2://'
if SQLALCHEMY_DATABASE_URL:
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# 3. Limpiar parámetros de SSL de la URL si existen para manejarlos en connect_args
# Esto evita duplicados o conflictos
if SQLALCHEMY_DATABASE_URL and "?sslmode=" in SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.split("?")[0]

# Debug sanitized URL
debug_url = SQLALCHEMY_DATABASE_URL
if debug_url and "@" in debug_url:
    debug_url = debug_url.split("@")[-1]
print(f"INFO: Intentando conectar a: {debug_url}")

# 4. Crear el motor (Engine) con configuraciones robustas para Render
# Usamos connect_args para pasar parámetros directamente al driver psycopg2
connect_args = {}
if SQLALCHEMY_DATABASE_URL and "localhost" not in SQLALCHEMY_DATABASE_URL:
    connect_args = {
        "sslmode": "require",
        "connect_timeout": 10  # Aumentamos el timeout para handshakes entre regiones
    }

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,     # Verifica que la conexión esté viva antes de usarla
    pool_recycle=300,       # Recicla conexiones cada 5 minutos
    pool_size=5,            # Limitamos el pool para evitar saturar la BD gratuita de Render
    max_overflow=10
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
