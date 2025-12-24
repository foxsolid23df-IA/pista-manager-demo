from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# ==========================================
# MÓDULO 1: PÚBLICO GENERAL (TAQUILLA)
# ==========================================

class Tarifa(Base):
    __tablename__ = "tarifas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)  # Ej: "Tiempo Libre", "Promoción Escolar"
    costo_base = Column(Float)            # Ej: 100.00
    minutos_base = Column(Integer)        # Ej: 60 minutos
    costo_minuto_extra = Column(Float)    # Ej: 2.00 por minuto extra
    activa = Column(Boolean, default=True)

    # Relación inversa (para saber cuántas sesiones usaron esta tarifa)
    sesiones = relationship("SesionPatinaje", back_populates="tarifa")


class SesionPatinaje(Base):
    __tablename__ = "sesiones_patinaje"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True) # Código de Barras / QR
    hora_entrada = Column(DateTime, nullable=True) # Se llena al CRUZAR EL TORNIQUETE
    hora_salida = Column(DateTime, nullable=True) # Se llena al salir
    
    monto_total = Column(Float, default=0.0)
    pagado = Column(Boolean, default=False)
    
    # --- NUEVOS CAMPOS PARA VENTA DE TAQUILLA ---
    # 1. Renta de Equipo
    renta_andadera = Column(Boolean, default=False) # ¿Pidió andadera?
    costo_andadera = Column(Float, default=50.0)    # Precio al momento de la venta
    
    # 2. Relación con Instructor (Opción directa en taquilla)
    tiene_instructor = Column(Boolean, default=False)
    instructor_id = Column(Integer, ForeignKey("instructores.id"), nullable=True)

    # NUEVO: Para saber si el dinero está en el cajón o en el banco
    metodo_pago = Column(String, default="Efectivo") # "Efectivo", "Tarjeta", "Transferencia"

    # Relaciones
    tarifa_id = Column(Integer, ForeignKey("tarifas.id"))
    tarifa = relationship("Tarifa", back_populates="sesiones")
    # Relación opcional para saber quién fue el instructor
    instructor = relationship("Instructor")

    # NUEVO: Cliente Frecuente (Opcional)
    cliente_id = Column(Integer, ForeignKey("clientes_frecuentes.id"), nullable=True)
    cliente = relationship("ClienteFrecuente", back_populates="sesiones")

# ==========================================
# MÓDULO 2: ESCUELA (ACTUALIZADO)
# ==========================================

class Instructor(Base):
    __tablename__ = "instructores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    especialidad = Column(String) # Ej: Hockey, Artístico
    activo = Column(Boolean, default=True)
    # NUEVO: Cuánto gana el profe por clase dada
    honorarios_por_sesion = Column(Float, default=150.0) 
    
    clases = relationship("Clase", back_populates="instructor")
    # Nueva relación con las rentas particulares
    rentas = relationship("RentaInstructor", back_populates="instructor")

# --- NUEVA TABLA: RENTA DE INSTRUCTORES ---
class RentaInstructor(Base):
    __tablename__ = "rentas_instructores"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamos esto con el Ticket del Patinador (SesionPatinaje)
    sesion_id = Column(Integer, ForeignKey("sesiones_patinaje.id"))
    instructor_id = Column(Integer, ForeignKey("instructores.id"))
    
    monto_cobrado_cliente = Column(Float) # Lo que pagó el cliente (ej. $200)
    monto_honorarios = Column(Float)      # Lo que le toca al profe (ej. $150)
    
    fecha_renta = Column(DateTime, default=datetime.now)
    
    # ESTADO CRÍTICO: 
    # 'Pendiente' = El cliente tiene el ticket, el profe no lo ha entregado.
    # 'Procesado' = El profe ya entregó el ticket y se contabilizó para su pago.
    estado_pago = Column(String, default="Pendiente") 
    
    instructor = relationship("Instructor", back_populates="rentas")
    sesion = relationship("SesionPatinaje") # Para saber qué ticket fue

class Alumno(Base):
    __tablename__ = "alumnos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono_contacto = Column(String)
    nivel = Column(String) # Ej: "Básico 1"
    fecha_nacimiento = Column(Date, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    # Campo calculado: ¿Hasta cuándo está pagado?
    # Esto ayuda a validar entrada rápido sin sumar todos los pagos cada vez
    vencimiento_mensualidad = Column(Date, nullable=True) 
    # Nuevo campo para saber disciplina
    disciplina = Column(String, default="Artistico") # "Artistico", "Hockey"
    
    pagos = relationship("PagoEscuela", back_populates="alumno")
    inscripciones = relationship("Inscripcion", back_populates="alumno")

# Nueva Tabla para Fiestas y Rentas de Pista
class ReservaEvento(Base):
    __tablename__ = "reservas_eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String) # "Fiesta", "RentaCompleta"
    nombre_cliente = Column(String)
    telefono = Column(String)
    fecha_evento = Column(DateTime) # Día y hora de la fiesta
    duracion_horas = Column(Integer)
    costo_total = Column(Float)
    anticipo_pagado = Column(Float, default=0.0)
    estado = Column(String, default="Confirmado") # Confirmado, Cancelado, Finalizado

class Clase(Base):
    __tablename__ = "clases"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String) # Ej: "Infantil Sabatino"
    dia_semana = Column(String) # "Sábado"
    hora_inicio = Column(String) # "10:00"
    instructor_id = Column(Integer, ForeignKey("instructores.id"))
    
    instructor = relationship("Instructor", back_populates="clases")
    inscripciones = relationship("Inscripcion", back_populates="clase")

class Inscripcion(Base):
    __tablename__ = "inscripciones"
    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"))
    clase_id = Column(Integer, ForeignKey("clases.id"))
    
    alumno = relationship("Alumno", back_populates="inscripciones")
    clase = relationship("Clase", back_populates="inscripciones")

class PagoEscuela(Base):
    __tablename__ = "pagos_escuela"
    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"))
    monto = Column(Float)
    fecha_pago = Column(DateTime, default=datetime.now)
    concepto = Column(String) # "Mensualidad Noviembre", "Inscripción"
    metodo_pago = Column(String, default="Efectivo") # "Efectivo", "Tarjeta"
    
    # Relación
    alumno = relationship("Alumno", back_populates="pagos")


# ==========================================
# MÓDULO 3: CLUB PISTA (CLIENTES FRECUENTES / FIDELIDAD)
# ==========================================

class ClienteFrecuente(Base):
    __tablename__ = "clientes_frecuentes"
    
    id = Column(Integer, primary_key=True, index=True)
    # Datos Personales (Mínimos necesarios para seguridad)
    nombre = Column(String)
    telefono = Column(String, unique=True, index=True) # Usaremos el Celular como ID único
    email = Column(String, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    # Sistema de Puntos
    puntos_acumulados = Column(Integer, default=0)
    nivel = Column(String, default="Bronce") # Bronce, Plata, Oro
    activo = Column(Boolean, default=True) # Para borrado lógico / derecho al olvido
    
    # Relación para saber su historial
    sesiones = relationship("SesionPatinaje", back_populates="cliente")
    movimientos_puntos = relationship("HistorialPuntos", back_populates="cliente")

class HistorialPuntos(Base):
    """Auditoría de Puntos: Para saber por qué subieron o bajaron"""
    __tablename__ = "historial_puntos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes_frecuentes.id"))
    
    puntos = Column(Integer) # Puede ser positivo (+50) o negativo (-100 canje)
    motivo = Column(String)  # "Visita Pista", "Canje Andadera", "Bono Cumpleaños"
    fecha = Column(DateTime, default=datetime.now)
    
    cliente = relationship("ClienteFrecuente", back_populates="movimientos_puntos")
