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
    
    # Escapamos usuario y contraseña por si tienen caracteres especiales (@, #, /)
    safe_user = urllib.parse.quote_plus(USER) if USER else ""
    safe_password = urllib.parse.quote_plus(PASSWORD) if PASSWORD else ""
    
    SQLALCHEMY_DATABASE_URL = f"postgresql://{safe_user}:{safe_password}@{SERVER}:{PORT}/{DB_NAME}"

# 2. Corrección de protocolo y dialecto
# Usamos pg8000 (Pure Python) para máxima compatibilidad con SSL y evitar errores de compilación
if SQLALCHEMY_DATABASE_URL:
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql+pg8000://", 1)
    elif SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)

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
