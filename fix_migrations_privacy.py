import sys
import os

# Agregar directorio actual al path
sys.path.append(os.getcwd())

from app.database import engine
from sqlalchemy import text

def migrate_loyalty_privacy():
    with engine.connect() as conn:
        print("--- Migración: Privacidad y Derecho al Olvido ---")
        
        try:
            conn.execute(text("ALTER TABLE clientes_frecuentes ADD COLUMN activo BOOLEAN DEFAULT TRUE"))
            print("✅ Columna 'activo' agregada a clientes_frecuentes.")
        except Exception as e:
            print(f"ℹ️ Nota: {e}")

        try:
            conn.commit()
            print("💾 Cambios de privacidad guardados.")
        except Exception as e:
            print(f"❌ Error al hacer commit: {e}")

if __name__ == "__main__":
    migrate_loyalty_privacy()
