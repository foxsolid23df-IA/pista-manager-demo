import sys
import os

# Agregar directorio actual al path
sys.path.append(os.getcwd())

from app.database import engine
from sqlalchemy import text

def migrate_loyalty():
    with engine.connect() as conn:
        print("--- Iniciando Migración Módulo de Lealtad (Club Pista) ---")
        
        # 1. Crear tabla Clientes Frecuentes
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS clientes_frecuentes (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR,
                    telefono VARCHAR UNIQUE,
                    email VARCHAR,
                    fecha_registro TIMESTAMP DEFAULT NOW(),
                    puntos_acumulados INTEGER DEFAULT 0,
                    nivel VARCHAR DEFAULT 'Bronce'
                )
            """))
            # Indices manually if needed, but SERIAL PRIMARY KEY handles id index
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_clientes_frecuentes_telefono ON clientes_frecuentes (telefono)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_clientes_frecuentes_id ON clientes_frecuentes (id)"))
            print("✅ Tabla 'clientes_frecuentes' asegurada.")
        except Exception as e:
            print(f"ℹ️ Nota sobre clientes_frecuentes: {e}")

        # 2. Crear tabla Historial Puntos
        try:
             conn.execute(text("""
                CREATE TABLE IF NOT EXISTS historial_puntos (
                    id SERIAL PRIMARY KEY,
                    cliente_id INTEGER REFERENCES clientes_frecuentes(id),
                    puntos INTEGER,
                    motivo VARCHAR,
                    fecha TIMESTAMP DEFAULT NOW()
                )
            """))
             conn.execute(text("CREATE INDEX IF NOT EXISTS ix_historial_puntos_id ON historial_puntos (id)"))
             print("✅ Tabla 'historial_puntos' asegurada.")
        except Exception as e:
            print(f"ℹ️ Nota sobre historial_puntos: {e}")

        # 3. Actualizar SesionPatinaje
        try:
            conn.execute(text("ALTER TABLE sesiones_patinaje ADD COLUMN cliente_id INTEGER NULL REFERENCES clientes_frecuentes(id)"))
            print("✅ Tabla 'sesiones_patinaje' actualizada con enlace a cliente frecuente.")
        except Exception as e:
            print(f"ℹ️ Nota sobre sesiones_patinaje (cliente_id): {e}")

        try:
            conn.commit()
            print("💾 Cambios de Módulo Lealtad guardados exitosamente.")
        except Exception as e:
            print(f"❌ Error al hacer commit: {e}")

if __name__ == "__main__":
    try:
        migrate_loyalty()
    except Exception as e:
        print(f"Error general en script: {e}")
