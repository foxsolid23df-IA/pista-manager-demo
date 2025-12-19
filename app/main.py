from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles # <--- NUEVO: Importar esto
from sqlalchemy.orm import Session
from datetime import datetime

# Importamos nuestros módulos anteriores
from . import models, schemas, crud
from .database import engine, get_db
from .services.calculadora import calcular_costo_final

# Inicializamos la App
app = FastAPI(title="Sistema Pista Hielo - PCTronicMex")

# Configuración de CORS (Indispensable para Frontend)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (localhost, IPs, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas si no existen (por seguridad)
models.Base.metadata.create_all(bind=engine)

# --- NUEVO: MONTAR CARPETA ESTÁTICA ---
# Esto hace que todo lo que pongas en la carpeta /static sea accesible via web
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

# --- INCLUIR ROUTERS ---
# --- INCLUIR ROUTERS ---
# --- INCLUIR ROUTERS ---
from .routers import escuela, instructores, acceso, reportes
app.include_router(escuela.router)
app.include_router(instructores.router)
app.include_router(acceso.router)
app.include_router(reportes.router)

# --- RUTAS (ENDPOINTS) ---

@app.get("/")
def home():
    return {"mensaje": "Servidor de Pista de Hielo Activo y Corriendo 🚀"}

@app.get("/tarifas/", response_model=list[schemas.TarifaResponse])
def listar_tarifas(db: Session = Depends(get_db)):
    """Muestra las tarifas disponibles para seleccionar en recepción"""
    tarifas = db.query(models.Tarifa).filter(models.Tarifa.activa == True).all()
    return tarifas

@app.post("/check-in/", response_model=schemas.TicketResponse)
def registrar_entrada(datos: schemas.EntradaRequest, db: Session = Depends(get_db)):
    """Genera ticket con: Tiempo + Andadera + Instructor"""
    
    # 1. Validar Tarifa (1 Hora, Tiempo Libre, etc.)
    tarifa = crud.get_tarifa_activa(db, datos.tarifa_id)
    if not tarifa:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    
    # 2. Generar ID único
    import uuid
    ticket_codigo = str(uuid.uuid4())[:8].upper()

    # 3. Preparar la Sesión
    nueva_sesion = models.SesionPatinaje(
        ticket_id=ticket_codigo,
        tarifa_id=datos.tarifa_id,
        renta_andadera=datos.renta_andadera,
        costo_andadera=50.0 if datos.renta_andadera else 0.0, # Precio fijo o buscar en BD
        instructor_id=datos.instructor_id,
        tiene_instructor=True if datos.instructor_id else False,
        metodo_pago=datos.metodo_pago
    )
    
    db.add(nueva_sesion)
    db.flush() # Guardamos temporalmente para obtener el ID de la sesión

    # 4. (MAGIA) Si pidió Instructor, crear la Renta automáticamente
    # Esto reemplaza el paso manual de "asignar instructor" que hicimos ayer
    if datos.instructor_id:
        # Buscamos cuánto cobra este profe
        profe = db.query(models.Instructor).filter(models.Instructor.id == datos.instructor_id).first()
        if profe:
            nueva_renta = models.RentaInstructor(
                sesion_id=nueva_sesion.id,
                instructor_id=profe.id,
                monto_cobrado_cliente=200.0, # Precio de la clase al cliente
                monto_honorarios=profe.honorarios_por_sesion,
                estado_pago="Pendiente"
            )
            db.add(nueva_renta)

    db.commit()
    
    # Calcular total a mostrar en el ticket
    total_inicial = tarifa.costo_base
    if datos.renta_andadera: total_inicial += 50.0
    if datos.instructor_id: total_inicial += 200.0 # Precio clase

    mensaje_extra = ""
    if datos.renta_andadera: mensaje_extra += " + 🐧 Andadera"
    if datos.instructor_id: mensaje_extra += " + ⛸️ Instructor"

    return {
        "ticket_id": ticket_codigo,
        "hora_entrada": nueva_sesion.hora_entrada,
        "mensaje": f"Entrada: {tarifa.nombre}{mensaje_extra}",
        "total_pagado": total_inicial
    }

@app.post("/check-out/", response_model=schemas.CobroResponse)
def registrar_salida(datos: schemas.SalidaRequest, db: Session = Depends(get_db)):
    """Calcula el cobro y cierra el ticket"""
    
    # 1. Buscar el ticket
    sesion = crud.buscar_sesion_por_ticket(db, datos.ticket_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Ticket no válido o ya pagado")
    
    # 2. Calcular cobro (Usando tu lógica del Día 3)
    # Nota: Si quisieras cobrar ANTES de cerrar, solo quitarías la línea de cerrar_sesion
    calculo = calcular_costo_final(
        hora_entrada=sesion.hora_entrada,
        hora_salida=datetime.now(),
        costo_base=sesion.tarifa.costo_base,
        minutos_base=sesion.tarifa.minutos_base,
        costo_extra=sesion.tarifa.costo_minuto_extra
    )
    
    # 3. Guardar cierre en BD
    crud.cerrar_sesion_patinador(db, sesion, calculo["total_a_pagar"])
    
    return {
        "ticket_id": sesion.ticket_id,
        "tiempo_total_min": calculo["minutos_totales"],
        "minutos_extra": calculo["minutos_extra"],
        "total_pagar": calculo["total_a_pagar"],
        "mensaje": "Ticket cerrado exitosamente"
    }

# ... (Tus imports deben incluir models y database)

@app.post("/admin/sembrar-datos-iniciales/")
def sembrar_datos(db: Session = Depends(get_db)):
    """
    Este botón crea las tarifas básicas si la base de datos está vacía.
    Úsalo solo una vez al desplegar.
    """
    # 1. Verificar si ya existen tarifas para no duplicar
    tarifas_existen = db.query(models.Tarifa).count()
    if tarifas_existen > 0:
        return {"mensaje": "⚠️ La base de datos ya tiene tarifas. No se hizo nada."}

    # 2. Crear Tarifas Básicas
    tarifa_hora = models.Tarifa(
        nombre="1 Hora",
        costo_base=100.0,
        minutos_base=60,
        costo_minuto_extra=2.5,
        activa=True
    )
    
    tarifa_libre = models.Tarifa(
        nombre="Tiempo Libre",
        costo_base=180.0,
        minutos_base=480, # 8 horas (simbólico)
        costo_minuto_extra=0.0,
        activa=True
    )

    # 3. Guardar en Base de Datos
    db.add(tarifa_hora)
    db.add(tarifa_libre)
    
    # Opcional: Crear también un Instructor de prueba
    profe = models.Instructor(
        nombre="Instructor Prueba",
        especialidad="General",
        honorarios_por_sesion=150.0,
        activo=True
    )
    db.add(profe)

    db.commit()
    
    return {"mensaje": "✅ ¡Datos iniciales sembrados con éxito! (Tarifas e Instructor creados)"}
