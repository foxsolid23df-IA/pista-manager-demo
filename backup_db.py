import os
import time
from datetime import datetime

# Configuración
CONTAINER_NAME = "pista_postgres"
DB_USER = "admin_pista" # Debe coincidir con tu .env
BACKUP_DIR = "backups"

def realizar_backup():
    # 1. Crear carpeta si no existe
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # 2. Nombre del archivo con fecha
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archivo = f"{BACKUP_DIR}/backup_pista_{fecha}.sql"

    print(f"⏳ Iniciando respaldo: {archivo}...")

    # 3. Ejecutar comando de Docker para volcar la BD
    # docker exec -t [contenedor] pg_dump -U [usuario] [bd] > [archivo]
    comando = f"docker exec -t {CONTAINER_NAME} pg_dump -U {DB_USER} pista_hielo_db > {archivo}"
    
    exit_code = os.system(comando)

    if exit_code == 0:
        print("✅ Respaldo exitoso.")
    else:
        print("❌ Error al crear el respaldo.")

if __name__ == "__main__":
    realizar_backup()
