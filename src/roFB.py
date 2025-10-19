# Codiguito para Solución por fuerza brurisisisisisima
from itertools import permutations
import time
import sys

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
    for idx in perm_v:
        print(idx)
    return mejor_costo
    
if __name__ == "__main__":
    
    if len(sys.argv) >1:
        for i in range(1, len(sys.argv)):
            main(f"src/{sys.argv[i]}.txt")
    else:
        main()
    