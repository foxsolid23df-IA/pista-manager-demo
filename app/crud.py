from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from . import models

# --- OPERACIONES DE TARIFA ---
def get_tarifa_activa(db: Session, tarifa_id: int):
    return db.query(models.Tarifa).filter(models.Tarifa.id == tarifa_id).first()

# --- OPERACIONES DE SESIÓN (Entrada/Salida) ---

def crear_entrada_patinador(db: Session, tarifa_id: int):
    """Genera un ticket nuevo y registra la hora de entrada"""
    
    # Generamos un ID de ticket único (como un código de barras)
    ticket_codigo = str(uuid.uuid4())[:8].upper() # Ej: "A1B2C3D4"
    
    nueva_sesion = models.SesionPatinaje(
        ticket_id=ticket_codigo,
        tarifa_id=tarifa_id,
        hora_entrada=datetime.now(),
        pagado=False
    )
    
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion

def buscar_sesion_por_ticket(db: Session, ticket_codigo: str):
    """Busca a alguien que esté patinando actualmente"""
    return db.query(models.SesionPatinaje).filter(
        models.SesionPatinaje.ticket_id == ticket_codigo,
        models.SesionPatinaje.pagado == False # Solo busca tickets abiertos
    ).first()

def cerrar_sesion_patinador(db: Session, sesion_obj: models.SesionPatinaje, monto: float):
    """Registra la salida y el monto final"""
    sesion_obj.hora_salida = datetime.now()
    sesion_obj.monto_total = monto
    sesion_obj.pagado = True # Opcional: podrías marcarlo pagado en otro paso
    
    db.commit()
    db.refresh(sesion_obj)
    return sesion_obj
