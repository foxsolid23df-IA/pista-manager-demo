from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# --- ESQUEMAS PARA ENTRADA DE DATOS (LO QUE RECIBES) ---

class EntradaRequest(BaseModel):
    tarifa_id: int
    renta_andadera: bool = False  # Checkbox en el frontend
    instructor_id: Optional[int] = None # Dropdown en el frontend (puede ser null)
    metodo_pago: str = "Efectivo" # NUEVO: "Efectivo" o "Tarjeta"

class SalidaRequest(BaseModel):
    ticket_id: str

# --- ESQUEMAS PARA RESPUESTA (LO QUE ENVÍAS AL CLIENTE) ---

class TarifaResponse(BaseModel):
    id: int
    nombre: str
    costo_base: float
    
    class Config:
        from_attributes = True

class TicketResponse(BaseModel):
    ticket_id: str
    hora_entrada: Optional[datetime]
    mensaje: str
    total_pagado: float # NUEVO: Para mostrar en el ticket

class CobroResponse(BaseModel):
    ticket_id: str
    tiempo_total_min: int
    minutos_extra: int
    total_pagar: float
    mensaje: str

# --- ESQUEMAS ESCUELA ---

class AlumnoCreate(BaseModel):
    nombre: str
    telefono_contacto: str
    nivel: str
    fecha_nacimiento: Optional[date] = None

class AlumnoResponse(BaseModel):
    id: int
    nombre: str
    nivel: str
    vencimiento_mensualidad: Optional[date]
    
    class Config:
        from_attributes = True

class PagoCreate(BaseModel):
    alumno_id: int
    monto: float
    concepto: str # Ej: "Mensualidad"
    dias_vigencia: int = 30 # Por defecto un mes

class InstructorCreate(BaseModel):
    nombre: str
    especialidad: str

class InstructorResponse(BaseModel):
    id: int
    nombre: str
    especialidad: str
    
    class Config:
        from_attributes = True

class ClaseCreate(BaseModel):
    nombre: str
    dia_semana: str
    hora_inicio: str
    instructor_id: int
    duracion_minutos: int = 60

class ClaseResponse(BaseModel):
    id: int
    nombre: str
    dia_semana: str
    hora_inicio: str
    
    class Config:
        from_attributes = True

# --- ESQUEMAS RENTA INSTRUCTORES ---

class AsignarInstructorRequest(BaseModel):
    ticket_id: str         # El código de barras del cliente
    instructor_id: int     # El ID del profe seleccionado

class ProcesarTicketRequest(BaseModel):
    ticket_id: str         # El ticket que el profe entrega en caja

class CorteInstructorResponse(BaseModel):
    instructor: str
    tickets_procesados: int
    total_honorarios: float
    detalle_tickets: list
