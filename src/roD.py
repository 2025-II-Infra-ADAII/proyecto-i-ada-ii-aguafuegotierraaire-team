
from itertools import permutations
from math import inf
from functools import lru_cache

def leer_finca(route):
    ruta = route
    with open(ruta, 'r') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]
    n = int(lineas[0])
    finca = [tuple(map(int, l.split(','))) for l in lineas[1:n+1]]

    return finca


def roDP(finca):
    """
    Resuelve el problema de optimización de riego usando programación dinámica.
    
    Args:
        tablones: Lista de tuplas (ts_i, tr_i, p_i) donde:
                  ts_i = tiempo de supervivencia (días)
                  tr_i = tiempo de regado (días)
                  p_i = prioridad (1-4)
    
    Returns:
        (costo_minimo, permutacion_optima)
    """
    n = len(finca)
    
    # Caso base
    if n == 0:
        return 0, []
    
    # dp[mask] = (costo_minimo, ultimo_tablon, tiempo_acumulado)
    # mask representa qué tablones ya han sido regados (bit i = 1 si tablón i regado)
    INF = float('inf')
    dp = {}
    
    # Estado inicial: ningún tablón regado
    dp[0] = (0, -1, 0)  # (costo, último tablón, tiempo acumulado)
    
    # Para cada estado (conjunto de tablones regados)
    for mask in range(1 << n):
        if mask not in dp:
            continue
            
        costo_actual, _, tiempo_actual = dp[mask]
        
        # Intentar regar cada tablón no regado
        for i in range(n):
            if mask & (1 << i):  # Si el tablón i ya fue regado
                continue
            
            # Nuevo estado: agregar tablón i
            nuevo_mask = mask | (1 << i)
            
            # Calcular tiempo de inicio para tablón i
            tiempo_inicio = tiempo_actual
            
            # Calcular tiempo de finalización
            ts_i, tr_i, p_i = finca[i]
            tiempo_fin = tiempo_inicio + tr_i
            
            # Calcular penalización
            retraso = max(0, tiempo_fin - ts_i)
            penalizacion = p_i * retraso
            
            # Nuevo costo y tiempo
            nuevo_costo = costo_actual + penalizacion
            nuevo_tiempo = tiempo_fin
            
            # Actualizar dp si es mejor
            if nuevo_mask not in dp or nuevo_costo < dp[nuevo_mask][0]:
                dp[nuevo_mask] = (nuevo_costo, i, nuevo_tiempo)
    
    # Reconstruir la solución
    mask_final = (1 << n) - 1
    if mask_final not in dp:
        return INF, []
    
    costo_minimo = dp[mask_final][0]
    
    # Reconstruir permutación
    permutacion = []
    mask_actual = mask_final
    
    while mask_actual > 0:
        _, ultimo, _ = dp[mask_actual]
        permutacion.append(ultimo)
        mask_actual ^= (1 << ultimo)  # Quitar el último tablón
    
    permutacion.reverse()
   
    return permutacion, int(costo_minimo)

def main(p):
    return roDP(leer_finca(p))[1]
    