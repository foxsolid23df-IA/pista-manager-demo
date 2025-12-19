from app.database import engine, Base
# Importamos TODOS los modelos para que SQLAlchemy los reconozca antes de crear la BD
from app import models 

def init_db():
    print("Conectando a la Base de Datos...")
    print("Creando tablas si no existen...")
    
    # Esta es la línea mágica: Crea las tablas definidas en models.py
    Base.metadata.create_all(bind=engine)
    
    print("¡Tablas creadas exitosamente!")
    print("Base de Datos lista para trabajar.")

if __name__ == "__main__":
    init_db()
