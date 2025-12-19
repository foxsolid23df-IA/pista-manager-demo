from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..services import cobro

router = APIRouter()

@router.post("/check-in/")
def entrada_patinador(ticket_id: str, tarifa_id: int, db: Session = Depends(get_db)):
    # 1. Crear sesión en BD
    nueva_sesion = models.SesionPatinaje(ticket_id=ticket_id, tarifa_id=tarifa_id)
    db.add(nueva_sesion)
    db.commit()
    return {"mensaje": "Entrada registrada", "hora": nueva_sesion.entrada}

@router.post("/check-out/")
def salida_patinador(ticket_id: str, db: Session = Depends(get_db)):
    # 1. Buscar sesión activa
    sesion = db.query(models.SesionPatinaje).filter(
        models.SesionPatinaje.ticket_id == ticket_id,
        models.SesionPatinaje.pagado == False
    ).first()
    
    if not sesion:
        raise HTTPException(status_code=404, detail="Ticket no encontrado o ya pagado")

    # 2. Usar el servicio de cálculo (Paso 3)
    monto = cobro.calcular_cobro(sesion, sesion.tarifa)
    
    # 3. Guardar en BD
    sesion.monto_total = monto
    sesion.pagado = True # Opcional: Esto podría ser en otro paso de "confirmar pago"
    db.commit()
    
    return {"ticket": ticket_id, "duracion_min": "...", "total_a_pagar": monto}
