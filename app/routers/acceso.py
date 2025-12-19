from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .. import database, models, crud
from ..services.calculadora import calcular_costo_final

router = APIRouter(prefix="/control-acceso", tags=["Acceso Torniquetes"])

@router.post("/validar-entrada/")
def validar_entrada(ticket_id: str, db: Session = Depends(database.get_db)):
    """Simula el escaneo en el torniquete de entrada"""
    
    # 1. Buscar ticket
    sesion = db.query(models.SesionPatinaje).filter(models.SesionPatinaje.ticket_id == ticket_id).first()
    
    if not sesion:
        raise HTTPException(status_code=404, detail="Ticket inválido")
    
    if sesion.hora_entrada is not None:
         # Si ya tiene hora de entrada, ¿es un reingreso o un error?
         # Por simplicidad, si ya entró hace menos de 5 min, lo dejamos pasar (fallo de dedo), 
         # si no, error.
         return {"estado": "YA_ADENTRO", "mensaje": "Este ticket ya está en uso dentro de la pista"}

    # 2. ACTIVAR EL TICKET (Aquí inicia el cronómetro real)
    sesion.hora_entrada = datetime.now()
    db.commit()
    
    return {
        "acceso": "PERMITIDO", 
        "mensaje": "Bienvenido, su tiempo comienza ahora.",
        "abre_torniquete": True
    }

@router.post("/validar-salida/")
def validar_salida(ticket_id: str, db: Session = Depends(database.get_db)):
    """Simula el escaneo para salir. Aquí se hace el 'Cierre de Compra'."""
    
    sesion = db.query(models.SesionPatinaje).filter(models.SesionPatinaje.ticket_id == ticket_id).first()
    
    if not sesion or not sesion.hora_entrada:
        raise HTTPException(status_code=400, detail="Ticket no registrado en la entrada")

    if sesion.pagado and sesion.monto_total > 0:
        return {"acceso": "DENEGADO", "mensaje": "Ticket ya finalizado anteriormente."}

    # 1. Calcular si debe algo
    calculo = calcular_costo_final(
        hora_entrada=sesion.hora_entrada,
        hora_salida=datetime.now(),
        costo_base=sesion.tarifa.costo_base,
        minutos_base=sesion.tarifa.minutos_base,
        costo_extra=sesion.tarifa.costo_minuto_extra
    )
    
    # 2. Verificar Deuda
    saldo_pendiente = calculo["total_a_pagar"] - sesion.tarifa.costo_base 
    # (Asumimos que el costo base ya se pagó al entrar)
    
    if saldo_pendiente > 0:
        # EL TORNIQUETE NO ABRE
        return {
            "acceso": "DENEGADO",
            "motivo": "TIEMPO_EXCEDIDO",
            "mensaje": f"Tiempo excedido por {int(calculo['minutos_extra'])} min.",
            "saldo_pendiente": saldo_pendiente,
            "abre_torniquete": False
        }
    
    # 3. Si todo está bien, cerramos el ticket
    sesion.hora_salida = datetime.now()
    sesion.monto_total = calculo["total_a_pagar"]
    sesion.pagado = True
    db.commit()

    return {
        "acceso": "PERMITIDO",
        "mensaje": "Gracias por su visita.",
        "abre_torniquete": True
    }
