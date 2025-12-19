from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Tarifa

db = SessionLocal()

# Verificar si ya existe alguna tarifa
existe = db.query(Tarifa).first()

if not existe:
    print("Creando tarifa por defecto...")
    nueva_tarifa = Tarifa(
        nombre="Hora Libre General",
        costo_base=100.0,
        minutos_base=60,
        costo_minuto_extra=2.5
    )
    db.add(nueva_tarifa)
    db.commit()
    print("Tarifa creada.")
else:
    print("Ya existen tarifas.")

db.close()
