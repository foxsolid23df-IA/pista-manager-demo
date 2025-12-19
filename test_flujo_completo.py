from app.database import SessionLocal
from app import crud
from app.services.calculadora import calcular_costo_final
from datetime import timedelta, datetime # Added datetime import to fix the script

# 1. Obtener conexión a BD
db = SessionLocal()

print("--- INICIO SIMULACIÓN ---")

# 2. Paso A: Llega un cliente y pide la Tarifa 1 (que creamos ayer)
print("1. Registrando entrada...")
try:
    sesion = crud.crear_entrada_patinador(db, tarifa_id=1)
    print(f"   >> Ticket Generado: {sesion.ticket_id}")
    print(f"   >> Hora Entrada: {sesion.hora_entrada}")
    
    # TRUCO DE VIAJE EN EL TIEMPO:
    # Vamos a "hackear" la hora de entrada para simular que entró hace 90 minutos
    # NO hagas esto en producción, es solo para probar el cálculo
    sesion.hora_entrada = sesion.hora_entrada - timedelta(minutes=90)
    db.commit()
    print("   >> (Simulación: Han pasado 90 minutos...)")

    # 3. Paso B: El cliente regresa el patín (Checkout)
    print("\n2. Procesando salida...")
    
    # Buscamos su tarifa para saber precios
    tarifa = sesion.tarifa 
    
    # Usamos nuestra calculadora (Capa de Lógica)
    # Nota: usamos datetime.now() como hora de salida real
    resultado = calcular_costo_final(
        hora_entrada=sesion.hora_entrada,
        hora_salida=sesion.hora_salida or datetime.now(), # Si no ha salido, usamos ahora
        costo_base=tarifa.costo_base,
        minutos_base=tarifa.minutos_base,
        costo_extra=tarifa.costo_minuto_extra
    )
    
    print(f"   >> Tiempo patinado: {resultado['minutos_totales']} min")
    print(f"   >> Minutos extra: {resultado['minutos_extra']} min")
    print(f"   >> TOTAL A PAGAR: ${resultado['total_a_pagar']}")
    
    # 4. Guardar en BD (Capa CRUD)
    sesion_cerrada = crud.cerrar_sesion_patinador(db, sesion, resultado['total_a_pagar'])
    print("\n3. Ticket cerrado y guardado en base de datos correctamente.")

except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
