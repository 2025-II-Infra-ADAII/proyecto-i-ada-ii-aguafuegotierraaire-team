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

def roD(finca):
    ts = [t._0 for t in finca]
    tr = [t._2 for t in finca]
    p = [t._3 for t in finca]
    """
    ts: lista de deadlines (tiempo de supervivencia) [ts_0, ...]
    tr: lista de duraciones de riego [tr_0, ...]
    p:  lista de prioridades (pesos) [p_0, ...]
    Devuelve: (min_cost, best_order) donde best_order es lista de indices en orden de riego.
    Requiere: tr, ts enteros y n pequeño (p.ej. n <= 18).
    """
    n = len(ts)
    T_total = sum(tr)

    @lru_cache(maxsize=None)
    def solve(mask, t):
        # mask: bits de tareas ya realizadas (1 = realizada)
        # t: tiempo actual (completación acumulada)
        if mask == (1 << n) - 1:
            return 0, ()   # costo 0 y orden vacío (ya no queda nada)
        best_cost = inf
        best_order = None
        # probar incluir cada trabajo no hecho en siguiente posición
        for i in range(n):
            if (mask >> i) & 1:
                continue
            new_t = t + tr[i]
            tardanza = max(0, new_t - ts[i])
            add_cost = p[i] * tardanza
            sub_cost, sub_order = solve(mask | (1 << i), new_t)
            total_cost = add_cost + sub_cost
            if total_cost < best_cost:
                best_cost = total_cost
                best_order = (i,) + sub_order
        return best_cost, best_order

    min_cost, order = solve(0, 0)
    return min_cost, order

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
    perm_DP, costo_DP = roV(finca)
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
    
