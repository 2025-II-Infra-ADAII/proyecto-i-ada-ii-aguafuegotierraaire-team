import math
from typing import List, Tuple

def resolver_riego_dp(tablones: List[Tuple[int, int, int]]) -> Tuple[int, List[int]]:
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
    n = len(tablones)
    
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
            ts_i, tr_i, p_i = tablones[i]
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
    
    return int(costo_minimo), permutacion



def mostrar_solucion(tablones: List[Tuple[int, int, int]], 
                     permutacion: List[int], 
                     costo: int):
    """
    Muestra la solución de forma detallada.
    """
    print(f"\n{'='*60}")
    print("SOLUCIÓN ÓPTIMA DE RIEGO")
    print(f"{'='*60}")
    print(f"\nCosto total mínimo: {costo}")
    print(f"\nOrden de riego: {permutacion}")
    print(f"\n{'Orden':<8}{'Tablón':<10}{'T.Inicio':<12}{'T.Fin':<10}{'Retraso':<10}{'Penaliz.':<10}")
    print("-" * 60)
    
    tiempo_actual = 0
    for orden, idx in enumerate(permutacion):
        ts_i, tr_i, p_i = tablones[idx]
        tiempo_inicio = tiempo_actual
        tiempo_fin = tiempo_inicio + tr_i
        retraso = max(0, tiempo_fin - ts_i)
        penalizacion = p_i * retraso
        
        print(f"{orden+1:<8}{idx:<10}{tiempo_inicio:<12}{tiempo_fin:<10}{retraso:<10}{penalizacion:<10}")
        
        tiempo_actual = tiempo_fin
    
    print("-" * 60)



if __name__ == "__main__":
    # Ejemplo 1: Caso simple
    print("\n" + "="*60)
    print("EJEMPLO 1: Caso Simple")
    print("="*60)
    
    # Tablones: (tiempo_supervivencia, tiempo_regado, prioridad)
    tablones1 = [
        (10, 3, 4),   # Tablón 0: sobrevive 5 días, toma 2 días regar, prioridad 3
        (5, 3, 3),   # Tablón 1: sobrevive 3 días, toma 1 día regar, prioridad 4
        (2, 2, 1),   # Tablón 2: sobrevive 6 días, toma 3 días regar, prioridad 2
        (8, 1, 1),   # Tablón 2: sobrevive 6 días, toma 3 días regar, prioridad 2
        (6, 4, 2),   # Tablón 2: sobrevive 6 días, toma 3 días regar, prioridad 2
    ]
