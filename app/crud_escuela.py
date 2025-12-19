from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas

def crear_alumno(db: Session, alumno: schemas.AlumnoCreate):
    nuevo_alumno = models.Alumno(
        nombre=alumno.nombre,
        telefono_contacto=alumno.telefono_contacto,
        nivel=alumno.nivel,
        fecha_nacimiento=alumno.fecha_nacimiento
    )
    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno)
    return nuevo_alumno

def get_alumnos(db: Session):
    return db.query(models.Alumno).all()

def registrar_pago(db: Session, pago: schemas.PagoCreate):
    # 1. Registrar el historial del pago
    nuevo_pago = models.PagoEscuela(
        alumno_id=pago.alumno_id,
        monto=pago.monto,
        concepto=pago.concepto,
        fecha_pago=datetime.now()
    )
    db.add(nuevo_pago)
    
    # 2. Actualizar la fecha de vencimiento del alumno
    # Buscamos al alumno
    alumno = db.query(models.Alumno).filter(models.Alumno.id == pago.alumno_id).first()
    
    if alumno:
        # Si ya tenía fecha vigente, sumamos días. Si no, empezamos desde hoy.
        inicio_vigencia = alumno.vencimiento_mensualidad
        if not inicio_vigencia or inicio_vigencia < datetime.now().date():
            inicio_vigencia = datetime.now().date()
            
        alumno.vencimiento_mensualidad = inicio_vigencia + timedelta(days=pago.dias_vigencia)
    
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

# --- CRUD INSTRUCTORES ---
def crear_instructor(db: Session, instructor: schemas.InstructorCreate):
    db_instructor = models.Instructor(
        nombre=instructor.nombre,
        especialidad=instructor.especialidad
    )
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def get_instructores(db: Session):
    return db.query(models.Instructor).filter(models.Instructor.activo == True).all()

def crear_clase(db: Session, clase: schemas.ClaseCreate):
    nueva_clase = models.Clase(
        nombre=clase.nombre,
        dia_semana=clase.dia_semana,
        hora_inicio=clase.hora_inicio,
        duracion_minutos=clase.duracion_minutos,
        instructor_id=clase.instructor_id
    )
    db.add(nueva_clase)
    db.commit()
    db.refresh(nueva_clase)
    return nueva_clase

def get_clases_calendario(db: Session):
    """
    Obtiene todas las clases y las formatea para FullCalendar.
    Devuelve eventos recurrentes semanales.
    """
    clases = db.query(models.Clase).all()
    eventos = []
    
    # Mapa para convertir "Lunes" a números (1=Lunes, 2=Martes...)
    dias_map = {
        "Domingo": 0, "Lunes": 1, "Martes": 2, "Miércoles": 3, 
        "Jueves": 4, "Viernes": 5, "Sábado": 6
    }

    for clase in clases:
        # Calcular hora fin (Asumimos 60 min si no se especifica)
        # Aquí podrías usar librerías de tiempo para ser más preciso
        hora_inicio_str = clase.hora_inicio # "16:00"
        try:
            h = int(hora_inicio_str.split(":")[0])
            hora_fin_str = f"{h+1}:00" 
        except:
             hora_fin_str = hora_inicio_str # Fallback simple

        eventos.append({
            "title": f"{clase.nombre} ({clase.instructor.nombre})",
            "startTime": f"{hora_inicio_str}:00",
            "endTime": f"{hora_fin_str}:00",
            "daysOfWeek": [dias_map.get(clase.dia_semana, 1)], # Repetir semanalmente
            "color": "#3788d8" # Azul para clases
        })
    
    return eventos
