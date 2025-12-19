from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT '¡Conexión Exitosa!'"))
        print(result.scalar())
except Exception as e:
    print(f"Error conectando: {e}")
