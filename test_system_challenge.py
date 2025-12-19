import requests
import datetime
import uuid
import sys

BASE_URL = "http://localhost:8000"

def log(msg, status="INFO"):
    colors = {
        "INFO": "\033[94m", # Blue
        "PASS": "\033[92m", # Green
        "FAIL": "\033[91m", # Red
        "WARN": "\033[93m"  # Yellow
    }
    end = "\033[0m"
    print(f"{colors.get(status, '')}[{status}] {msg}{end}")

def test_full_flow():
    print("\n" + "="*50)
    log("INICIANDO PROTOCOLO DE PRUEBAS DE SISTEMA", "INFO")
    print("="*50)
    
    # ---------------------------------------------------------
    # 1. SETUP DE DATOS
    # ---------------------------------------------------------
    try:
        r = requests.get(f"{BASE_URL}/tarifas/")
        if r.status_code != 200:
            log("No hay conexión con el servidor. ¿Docker está corriendo?", "FAIL")
            return
        
        tarifas = r.json()
        if not tarifas:
            log("No existen tarifas configuradas.", "FAIL")
            return
            
        tarifa_id = tarifas[0]['id']
        costo_base = tarifas[0]['costo_base']
        log(f"Conexión exitosa. Tarifa Base: ${costo_base}", "PASS")
    except Exception as e:
        log(f"Excepción de conexión: {e}", "FAIL")
        return

    tickets_creados = []
    
    # ---------------------------------------------------------
    # 2. PRUEBAS DE TAQUILLA (GENERACIÓN DE VENTA)
    # ---------------------------------------------------------
    print("\n--- 🛒 MÓDULO TAQUILLA ---")
    
    # PRUEBA 1: Venta ESTÁNDAR (Efectivo)
    try:
        payload = {
            "tarifa_id": tarifa_id,
            "renta_andadera": False,
            "instructor_id": None,
            "metodo_pago": "Efectivo"
        }
        r = requests.post(f"{BASE_URL}/check-in/", json=payload)
        if r.status_code == 200:
            data = r.json()
            tickets_creados.append(data)
            log(f"Venta Efectivo generada (Ticket: {data['ticket_id']})", "PASS")
            
            # Validar cálculo
            if data['total_pagado'] == costo_base:
                log(f"   └── Cálculo correcto: ${data['total_pagado']}", "PASS")
            else:
                log(f"   └── Error de cálculo: Esperaba ${costo_base}, obtuvo ${data['total_pagado']}", "FAIL")
        else:
            log(f"Error generando venta efectivo: {r.text}", "FAIL")
            
        # PRUEBA 2: Venta COMPLEJA (Tarjeta + Andadera)
        payload2 = {
            "tarifa_id": tarifa_id,
            "renta_andadera": True,
            "instructor_id": None, # Simplificamos sin instructor para esta prueba
            "metodo_pago": "Tarjeta"
        }
        r2 = requests.post(f"{BASE_URL}/check-in/", json=payload2)
        if r2.status_code == 200:
            data2 = r2.json()
            tickets_creados.append(data2)
            log(f"Venta Tarjeta+Andadera generada (Ticket: {data2['ticket_id']})", "PASS")
            
            esperado = costo_base + 50.0 # 50 de andadera
            if data2['total_pagado'] == esperado:
                log(f"   └── Cálculo correcto: ${data2['total_pagado']}", "PASS")
            else:
                log(f"   └── Error de cálculo: Esperaba ${esperado}, obtuvo ${data2['total_pagado']}", "FAIL")
        else:
            log(f"Error generando venta compleja: {r2.text}", "FAIL")

    except Exception as e:
        log(f"Excepción en Taquilla: {e}", "FAIL")

    if not tickets_creados:
        log("No hay tickets para probar Acceso. Abortando.", "FAIL")
        return

    # ---------------------------------------------------------
    # 3. PRUEBAS DE ACCESO (TORNIQUETES)
    # ---------------------------------------------------------
    print("\n--- 🚧 MÓDULO ACCESO ---")
    ticket_valido = tickets_creados[0]['ticket_id']
    ticket_sin_entrar = tickets_creados[1]['ticket_id']
    
    # PRUEBA 3: Entrada Válida
    r_ent = requests.post(f"{BASE_URL}/control-acceso/validar-entrada/?ticket_id={ticket_valido}")
    if r_ent.status_code == 200:
        log(f"Entrada permitida para Ticket {ticket_valido}", "PASS")
    else:
        log(f"Error en entrada válida: {r_ent.text}", "FAIL")

    # PRUEBA 4: Bloqueo de Re-ingreso (Anti-Passback)
    r_re = requests.post(f"{BASE_URL}/control-acceso/validar-entrada/?ticket_id={ticket_valido}")
    data_re = r_re.json()
    if data_re.get('estado') == "YA_ADENTRO":
        log(f"Bloqueo de doble uso (Re-ingreso) funcionando", "PASS")
    else:
        log(f"Fallo seguridad: Permitío reingreso o error distinto ({data_re})", "WARN")

    # PRUEBA 5: Ticket No Existente
    r_fake = requests.post(f"{BASE_URL}/control-acceso/validar-entrada/?ticket_id=PATO_DONALD")
    if r_fake.status_code == 404:
        log("Ticket falso rechazado correctamente (404)", "PASS")
    else:
        log("Sistema aceptó ticket falso o dio error incorrecto", "FAIL")

    # PRUEBA 6: Salida Válida
    r_sal = requests.post(f"{BASE_URL}/control-acceso/validar-salida/?ticket_id={ticket_valido}")
    if r_sal.status_code == 200:
        data_sal = r_sal.json()
        if data_sal.get("acceso") == "PERMITIDO":
            log(f"Salida Ticket {ticket_valido} exitosa", "PASS")
        else:
            log(f"Salida denegada (posible saldo pendiente): {data_sal}", "WARN")
    else:
        log(f"Error técnico en salida: {r_sal.text}", "FAIL")

    # PRUEBA 7: Salida de Ticket "Fantasma" (Nunca entró)
    r_sal_fake = requests.post(f"{BASE_URL}/control-acceso/validar-salida/?ticket_id={ticket_sin_entrar}")
    if r_sal_fake.status_code == 400:
        log("Seguridad correcta: No se puede salir si no se ha registrado entrada", "PASS")
    else:
        log(f"Fallo lógica: Permitió salir a alguien que no entró ({r_sal_fake.status_code})", "FAIL")

    # ---------------------------------------------------------
    # 4. PRUEBAS DE CIERRE DE DÍA (CONTABILIDAD)
    # ---------------------------------------------------------
    print("\n--- 💰 MÓDULO FINANCIERO ---")
    today = datetime.date.today().isoformat()
    r_corte = requests.get(f"{BASE_URL}/reportes/cierre-dia/?fecha_consulta={today}")
    
    if r_corte.status_code == 200:
        rep = r_corte.json()
        log("Reporte generado exitosamente", "PASS")
        
        # Validar consistencia básica
        total_reportado = rep['resumen_general']['total_ingresos']
        suma_desglosada = rep['resumen_general']['dinero_en_caja'] + rep['resumen_general']['dinero_banco']
        
        if total_reportado == suma_desglosada:
            log(f"Matemática Financiera Cuadra: ${total_reportado}", "PASS")
        else:
            log(f"Discrepancia contable: Total ${total_reportado} != Suma ${suma_desglosada}", "FAIL")
            
        # Validar Andaderas
        andaderas_ingreso = rep['desglose_taquilla']['ingreso_andaderas']
        if andaderas_ingreso >= 50.0: # Generamos al menos 1
             log(f"Ingreso de Andaderas registrado: ${andaderas_ingreso}", "PASS")
        else:
             log(f"No se registró el ingreso de andaderas (Esperaba >= 50, tiene {andaderas_ingreso})", "FAIL")
             
    else:
        log(f"Fallo al generar reporte: {r_corte.text}", "FAIL")

    print("\n" + "="*50)
    log("FIN DEL REPORTE AUTOMATIZADO", "INFO")
    print("="*50)

if __name__ == "__main__":
    test_full_flow()
