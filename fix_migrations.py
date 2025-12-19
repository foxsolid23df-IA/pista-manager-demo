import sys
import os

# Agregar directorio actual al path
sys.path.append(os.getcwd())

from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        print("--- Iniciando Migración Manual de Base de Datos ---")
        
        # 1. Actualizar SesionPatinaje
        try:
            # Postgres usa ADD COLUMN
            conn.execute(text("ALTER TABLE sesiones_patinaje ADD COLUMN metodo_pago VARCHAR DEFAULT 'Efectivo'"))
            # Asegurar que los nulos sean efectivo
            conn.execute(text("UPDATE sesiones_patinaje SET metodo_pago = 'Efectivo' WHERE metodo_pago IS NULL"))
            print("✅ Tabla 'sesiones_patinaje' actualizada con 'metodo_pago'.")
        except Exception as e:
            # Si falla, probablemente ya existe
            print(f"ℹ️ Nota sobre sesiones_patinaje: {e}")

        # 2. Actualizar PagoEscuela
        try:
            conn.execute(text("ALTER TABLE pagos_escuela ADD COLUMN metodo_pago VARCHAR DEFAULT 'Efectivo'"))
            conn.execute(text("UPDATE pagos_escuela SET metodo_pago = 'Efectivo' WHERE metodo_pago IS NULL"))
            print("✅ Tabla 'pagos_escuela' actualizada con 'metodo_pago'.")
        except Exception as e:
            print(f"ℹ️ Nota sobre pagos_escuela: {e}")
        
        try:
            conn.commit()
            print("💾 Cambios guardados exitosamente.")
        except Exception as e:
            print(f"❌ Error al hacer commit: {e}")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"Error general en script: {e}")
