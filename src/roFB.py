# Codiguito para Solución por fuerza brurisisisisisima
from itertools import permutations
import time
import sys
from math import inf
from functools import lru_cache

def leer_finca(r):
    ruta = r
    with open(ruta, 'r') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]
    n = int(lineas[0])
    finca = [tuple(map(int, l.split(','))) for l in lineas[1:n+1]]
    print(finca)
    return finca



def calcular_tiempos_inicio(finca, permutacion):
    tiempos = {}
    tiempo_actual = 0
    
    for tablon in permutacion:
        tiempos[tablon] = tiempo_actual
        tr = finca[tablon][1]
        tiempo_actual += tr
    
    return tiempos

def calculoCostoPerm(finca, permutacion):
    tiempos_inicio = calcular_tiempos_inicio(finca, permutacion)
    costo_total = 0
    for tablon in range(len(finca)):
        ts, tr, p = finca[tablon]
        t_inicio = tiempos_inicio[tablon]  
        t_fin_riego = t_inicio + tr
        penalizacion = p * max(0, t_fin_riego - ts)
        costo_total += penalizacion
    return costo_total


def roFB(finca):
    n = len(finca)
    if n == 0:
        return ([], 0)
    
    indices = list(range(n))
    mejor_costo = float('inf')
    mejor_permutacion = None

    for permutacion in permutations(indices):
        costo = calculoCostoPerm(finca, permutacion)
        if costo < mejor_costo:
            mejor_costo = costo
            mejor_permutacion = permutacion
    
    return (list(mejor_permutacion), mejor_costo)

def roV(finca):
    """
    Algoritmo voraz:
    Ordena los tablones por la razón p/ts descendente (mayor prioridad y menor tiempo de supervivencia primero),
    en caso de empate, por menor tiempo de riego (tr).
    Devuelve (permutacion, costo)
    """
    n = len(finca)
    if n == 0:
        return ([], 0)

    # Orden voraz: prioridad alta y supervivencia baja primero
    indices_ordenados = sorted(range(n),
                               key=lambda i: (-finca[i][2] / finca[i][0], finca[i][1]))

    # Calculamos costo igual que en fuerza bruta
    costo = calculoCostoPerm(finca, indices_ordenados)
    return (indices_ordenados, costo)

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

def main(r='src/finca.txt'):
    # === BLOQUE FUERZA BRUTA ===
    finca = leer_finca(r)
    tiempo_i = time.time()
    mejor_permutacion, mejor_costo = roFB(finca)
    tiempo_f = time.time()

    print("=======================================================================")
    print("RESULTADO ÓPTIMO")
    print("=======================================================================")
    print("Tiempo de ejecución:", tiempo_f - tiempo_i)
    
    print(mejor_costo)
    for idx in mejor_permutacion:
        print(idx)

     # === BLOQUE VORAZ ===
    tiempo_i_v = time.time()
    perm_v, costo_v = roV(finca)
    tiempo_f_v = time.time()

    print("\n=======================================================================")
    print("RESULTADO VORAZ")
    print("=======================================================================")
    print("Tiempo de ejecución:", tiempo_f_v - tiempo_i_v)
    print(costo_v)

    # === BLOQUE DINAMICO ===
    tiempo_i_DP = time.time()
    perm_DP, costo_DP = roDP(finca)
    tiempo_f_DP = time.time()
    for idx in perm_v:
        print(idx)

    print("\n=======================================================================")
    print("RESULTADO DINAMICO")
    print("=======================================================================")
    print("Tiempo de ejecución:", tiempo_f_DP - tiempo_i_DP)
    print(costo_DP)
    for idx in perm_DP:
        print(idx)
    return mejor_costo
    
if __name__ == "__main__":
    
    if len(sys.argv) >1:
        for i in range(1, len(sys.argv)):
            main(f"src/{sys.argv[i]}.txt")
    else:
        main()
    
