from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, extract
from datetime import datetime
from .. import database, models, schemas

router = APIRouter(prefix="/lealtad", tags=["Programa Lealtad"])

# 1. REGISTRO RÁPIDO (Solo pide Celular y Nombre)
@router.post("/registro/")
def registrar_cliente(nombre: str, telefono: str, db: Session = Depends(database.get_db)):
    existe = db.query(models.ClienteFrecuente).filter(models.ClienteFrecuente.telefono == telefono).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este teléfono ya está registrado")
    
    nuevo = models.ClienteFrecuente(nombre=nombre, telefono=telefono)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo) # Actualizar para obtener ID y defaults
    return {"mensaje": "¡Bienvenido al Club!", "id": nuevo.id, "puntos": 0}

# 2. BUSCAR CLIENTE (Para el Check-in)
@router.get("/buscar/{telefono}")
def buscar_cliente(telefono: str, db: Session = Depends(database.get_db)):
    cliente = db.query(models.ClienteFrecuente).filter(
        models.ClienteFrecuente.telefono == telefono,
        models.ClienteFrecuente.activo == True
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# 3. TOP CLIENTES (Detectar quién visita más)
@router.get("/top-visitantes/")
def top_clientes(limit: int = 10, db: Session = Depends(database.get_db)):
    """Devuelve la lista de clientes con más puntos acumulados"""
    return db.query(models.ClienteFrecuente).order_by(desc(models.ClienteFrecuente.puntos_acumulados)).limit(limit).all()

# 4. CANJEAR PUNTOS (Premiar)
@router.post("/canjear/")
def canjear_premio(cliente_id: int, costo_puntos: int, premio: str, db: Session = Depends(database.get_db)):
    cliente = db.query(models.ClienteFrecuente).filter(models.ClienteFrecuente.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if cliente.puntos_acumulados < costo_puntos:
        raise HTTPException(status_code=400, detail="Puntos insuficientes")
    
    # Restar puntos
    cliente.puntos_acumulados -= costo_puntos
    
    # Guardar en historial
    log = models.HistorialPuntos(
        cliente_id=cliente.id,
        puntos=-costo_puntos, # Negativo porque es resta
        motivo=f"Canje: {premio}"
    )
    db.add(log)
    db.commit()
    
    return {"mensaje": "Canje exitoso", "saldo_actual": cliente.puntos_acumulados}

# 5. DERECHO AL OLVIDO (GDPR / ARCO)
@router.delete("/eliminar-datos/{cliente_id}")
def eliminar_datos_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    cliente = db.query(models.ClienteFrecuente).filter(models.ClienteFrecuente.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
    # Anonimizar datos (Soft Delete)
    # Conservamos el ID y el historial de transacciones financieras (puntos), pero borramos la identidad.
    cliente.nombre = "Usuario Eliminado"
    cliente.telefono = f"DEL-{cliente.id}-{cliente.telefono[-4:]}" # Liberamos el teléfono único (más o menos)
    cliente.email = None
    cliente.activo = False
    
    db.commit()
    db.commit()
    return {"mensaje": "Datos personales eliminados correctamente. El historial se mantiene anónimo."}

# 6. REPORTE TOP MENSUAL (LEADERBOARD)
@router.get("/top-mensual/")
def reporte_top_clientes(mes: int = None, anio: int = None, db: Session = Depends(database.get_db)):
    """
    Busca quiénes han sumado más puntos (gastado más dinero) en un mes específico.
    Si no se envía fecha, usa el mes actual.
    """
    if not mes: mes = datetime.now().month
    if not anio: anio = datetime.now().year

    # Consulta SQL Avanzada:
    # 1. Filtramos historial de puntos positivos (ganancias) del mes/año
    # 2. Agrupamos por cliente
    # 3. Sumamos los puntos ganados
    ranking = db.query(
        models.ClienteFrecuente.nombre,
        models.ClienteFrecuente.telefono,
        func.sum(models.HistorialPuntos.puntos).label("puntos_ganados"),
        func.count(models.HistorialPuntos.id).label("visitas")
    ).join(models.HistorialPuntos).filter(
        extract('month', models.HistorialPuntos.fecha) == mes,
        extract('year', models.HistorialPuntos.fecha) == anio,
        models.HistorialPuntos.puntos > 0 # Solo puntos ganados, no canjes
    ).group_by(models.ClienteFrecuente.id, models.ClienteFrecuente.nombre, models.ClienteFrecuente.telefono)\
    .order_by(desc("puntos_ganados"))\
    .limit(10).all()

    # Formatear respuesta JSON
    resultado = []
    for row in ranking:
        resultado.append({
            "nombre": row.nombre,
            "telefono": row.telefono,
            "puntos_mes": row.puntos_ganados,
            "dinero_estimado": row.puntos_ganados * 10, # Si 1 pto = $10 pesos
            "visitas": row.visitas
        })
    
    return resultado
