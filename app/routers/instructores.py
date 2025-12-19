from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from .. import database, models, schemas, crud

router = APIRouter(prefix="/gestion-instructores", tags=["Instructores Rentas"])

# 1. ASIGNAR INSTRUCTOR (Cuando el cliente paga en caja)
@router.post("/asignar/")
def asignar_instructor(datos: schemas.AsignarInstructorRequest, db: Session = Depends(database.get_db)):
    # Buscar la sesión del patinador por su ticket
    sesion = db.query(models.SesionPatinaje).filter(models.SesionPatinaje.ticket_id == datos.ticket_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Ticket de patinador no encontrado")
    
    # Buscar al instructor para saber sus honorarios
    profe = db.query(models.Instructor).filter(models.Instructor.id == datos.instructor_id).first()
    if not profe:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    # Crear el registro de renta
    nueva_renta = models.RentaInstructor(
        sesion_id=sesion.id,
        instructor_id=profe.id,
        monto_cobrado_cliente=200.0, # Aquí podrías buscar el precio en otra tabla de tarifas
        monto_honorarios=profe.honorarios_por_sesion,
        estado_pago="Pendiente"
    )
    
    db.add(nueva_renta)
    db.commit()
    
    return {"mensaje": f"Instructor {profe.nombre} asignado al ticket {datos.ticket_id}"}

# 2. PROCESAR TICKET (Cuando el profe entrega el ticket en taquilla)
@router.post("/procesar-ticket/")
def procesar_ticket_instructor(datos: schemas.ProcesarTicketRequest, db: Session = Depends(database.get_db)):
    # Buscamos la renta ligada a ese ticket
    renta = db.query(models.RentaInstructor).join(models.SesionPatinaje).filter(
        models.SesionPatinaje.ticket_id == datos.ticket_id,
        models.RentaInstructor.estado_pago == "Pendiente"
    ).first()
    
    if not renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada o ticket ya procesado")
    
    # Marcamos como procesado
    renta.estado_pago = "Procesado"
    # renta.fecha_procesado = datetime.now() # Opcional: agregar campo fecha_procesado al modelo
    
    db.commit()
    
    return {
        "mensaje": "Ticket validado exitosamente",
        "instructor": renta.instructor.nombre,
        "honorarios_sumados": renta.monto_honorarios
    }

# 3. CORTE DEL DÍA POR INSTRUCTOR (Para pagarle sus honorarios)
@router.get("/corte-dia/{instructor_id}")
def obtener_corte_instructor(instructor_id: int, db: Session = Depends(database.get_db)):
    # Obtenemos solo los tickets PROCESADOS hoy (o todos los pendientes de pago)
    # Aquí asumimos que se paga lo del día.
    
    hoy = datetime.now().date()
    
    rentas = db.query(models.RentaInstructor).filter(
        models.RentaInstructor.instructor_id == instructor_id,
        models.RentaInstructor.estado_pago == "Procesado",
        # models.RentaInstructor.fecha_renta >= hoy # Descomentar para filtrar solo hoy
    ).all()
    
    total = sum(r.monto_honorarios for r in rentas)
    tickets = [r.sesion.ticket_id for r in rentas]
    
    return {
        "instructor_id": instructor_id,
        "tickets_procesados": len(rentas),
        "total_honorarios": total,
        "lista_tickets": tickets
    }
