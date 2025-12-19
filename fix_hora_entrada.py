import sys
import os

sys.path.append(os.getcwd())
from app.database import engine
from sqlalchemy import text

def fix_hora_entrada():
    with engine.connect() as conn:
        print("--- Ajustando Columna hora_entrada ---")
        try:
            # Eliminar valor por defecto (para que sea NULL al crear)
            conn.execute(text("ALTER TABLE sesiones_patinaje ALTER COLUMN hora_entrada DROP DEFAULT"))
            print("✅ Default eliminado.")
        except Exception as e:
            print(f"ℹ️ {e}")

        try:
            # Permitir Nulos
            conn.execute(text("ALTER TABLE sesiones_patinaje ALTER COLUMN hora_entrada DROP NOT NULL"))
            print("✅ Nullable activado.")
        except Exception as e:
            print(f"ℹ️ {e}")
            
        conn.commit()
        print("💾 Cambios guardados.")

if __name__ == "__main__":
    fix_hora_entrada()
