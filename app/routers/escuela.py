from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, crud_escuela

# Creamos un router específico para escuela
router = APIRouter(
    prefix="/escuela",
    tags=["Escuela"]
)

@router.post("/alumnos/", response_model=schemas.AlumnoResponse)
def crear_nuevo_alumno(alumno: schemas.AlumnoCreate, db: Session = Depends(database.get_db)):
    return crud_escuela.crear_alumno(db, alumno)

@router.get("/alumnos/", response_model=List[schemas.AlumnoResponse])
def listar_alumnos(db: Session = Depends(database.get_db)):
    return crud_escuela.get_alumnos(db)

@router.post("/pagos/")
def cobrar_mensualidad(pago: schemas.PagoCreate, db: Session = Depends(database.get_db)):
    """Registra pago y extiende la fecha de vencimiento del alumno"""
    nuevo_pago = crud_escuela.registrar_pago(db, pago)
    return {"mensaje": "Pago registrado correctamente", "id_pago": nuevo_pago.id}

@router.get("/instructores/", response_model=List[schemas.InstructorResponse])
def listar_instructores(db: Session = Depends(database.get_db)):
    return crud_escuela.get_instructores(db)

@router.post("/instructores/", response_model=schemas.InstructorResponse)
def nuevo_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(database.get_db)):
    return crud_escuela.crear_instructor(db, instructor)

@router.post("/clases/", response_model=schemas.ClaseResponse)
def crear_nueva_clase(clase: schemas.ClaseCreate, db: Session = Depends(database.get_db)):
    return crud_escuela.crear_clase(db, clase)

@router.get("/calendario/")
def obtener_calendario(db: Session = Depends(database.get_db)):
    """Devuelve los eventos para el frontend"""
    return crud_escuela.get_clases_calendario(db)

# --- NUEVOS ENDPOINTS PARA FIESTAS Y MENSUALIDADES ESPECIFICAS ---
from datetime import datetime
from .. import models

@router.post("/pagos/mensualidad/")
def cobrar_mensualidad_especifica(pago: schemas.PagoCreate, disciplina: str, db: Session = Depends(database.get_db)):
    """
    Cobra mensualidad y actualiza si es Hockey o Artístico.
    Usa el esquema PagoCreate pero añadimos lógica.
    """
    # Registramos el pago
    crud_escuela.registrar_pago(db, pago)
    
    # Actualizamos la disciplina del alumno si cambió
    alumno = db.query(models.Alumno).filter(models.Alumno.id == pago.alumno_id).first()
    if alumno:
        alumno.disciplina = disciplina # Ej: "Hockey"
        db.commit()
        
    return {"mensaje": f"Mensualidad de {disciplina} registrada exitosamente"}

@router.post("/reservas/")
def crear_reserva_evento(tipo: str, cliente: str, fecha: datetime, horas: int, costo: float, anticipo: float, db: Session = Depends(database.get_db)):
    """
    Agenda una fiesta o renta de pista completa.
    """
    nueva_reserva = models.ReservaEvento(
        tipo=tipo,
        nombre_cliente=cliente,
        fecha_evento=fecha,
        duracion_horas=horas,
        costo_total=costo,
        anticipo_pagado=anticipo
    )
    db.add(nueva_reserva)
    db.commit()
    return {"mensaje": f"Reserva de {tipo} creada para el {fecha}"}
