import math
from datetime import datetime, timedelta

def calcular_costo_final(hora_entrada: datetime, hora_salida: datetime, costo_base: float, minutos_base: int, costo_extra: float) -> dict:
    """
    Calcula el tiempo total y el monto a pagar.
    Retorna un diccionario con el desglose.
    """
    # 1. Calcular duración total en minutos
    diferencia = hora_salida - hora_entrada
    total_minutos = diferencia.total_seconds() / 60
    
    # Redondear hacia arriba (si patinó 60.1 minutos, se cobran 61)
    # Opcional: dependerá de tu regla de negocio, aquí usamos redondeo estándar
    total_minutos_redondeado = math.ceil(total_minutos)

    monto_final = 0.0
    minutos_extra = 0
    monto_extra_total = 0.0

    # 2. Aplicar reglas
    if total_minutos_redondeado <= minutos_base:
        # Si estuvo menos del tiempo base (ej. 1 hora), paga el base
        monto_final = costo_base
    else:
        # Si se pasó, calculamos el extra
        minutos_extra = total_minutos_redondeado - minutos_base
        monto_extra_total = minutos_extra * costo_extra
        monto_final = costo_base + monto_extra_total

    return {
        "minutos_totales": total_minutos_redondeado,
        "minutos_extra": minutos_extra,
        "costo_base": costo_base,
        "costo_extra": monto_extra_total,
        "total_a_pagar": monto_final
    }
