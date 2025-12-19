import requests
import sys

BASE_URL = "http://localhost:8000"

def test_ticket_generation():
    print("--- 1. Checking Tariffs ---")
    try:
        r = requests.get(f"{BASE_URL}/tarifas/")
        tarifas = r.json()
        print(f"Found {len(tarifas)} tariffs.")
        for t in tarifas:
            print(f"ID: {t['id']}, Name: {t['nombre']}, Cost: {t['costo_base']}")
        
        if not tarifas:
            print("❌ No tariffs found! Run sembrar_datos.py")
            return

        tarifa_id = tarifas[0]['id']
        costo_esperado = tarifas[0]['costo_base']
        
        print("\n--- 2. Simulating Check-in ---")
        payload = {
            "tarifa_id": tarifa_id,
            "renta_andadera": False,
            "instructor_id": None,
            "metodo_pago": "Efectivo"
        }
        
        r_ticket = requests.post(f"{BASE_URL}/check-in/", json=payload)
        if r_ticket.status_code != 200:
            print(f"❌ Error in check-in: {r_ticket.text}")
            return
            
        data = r_ticket.json()
        print("Response Data:", data)
        
        total_pagado = data.get("total_pagado")
        print(f"Total Pagado received: {total_pagado}")
        
        if total_pagado == costo_esperado:
            print(f"✅ SUCCESS: Total matches base cost ({costo_esperado})")
        else:
            print(f"❌ FAILURE: Expected {costo_esperado}, got {total_pagado}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ticket_generation()
