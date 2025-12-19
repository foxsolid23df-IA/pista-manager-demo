from datetime import datetime
import math

def calcular_cobro(sesion, tarifa):
    """
    Recibe un objeto Sesion y un objeto Tarifa.
    Retorna el monto a pagar.
    """
    if not sesion.salida:
        sesion.salida = datetime.now()
    
    # Calcular duración en minutos
    duracion = (sesion.salida - sesion.entrada).total_seconds() / 60
    
    # Si patinó menos del tiempo base, cobra el base
    if duracion <= tarifa.minutos_base:
        return tarifa.costo_base
    
    # Calcular extra
    minutos_extra = math.ceil(duracion - tarifa.minutos_base)
    cobro_extra = minutos_extra * tarifa.costo_minuto_extra
    
    return tarifa.costo_base + cobro_extra
