# Codiguito para Solución por fuerza brutisisisisisima
from itertools import permutations
import time as tm

def leer_finca(route):
    ruta = route
    with open(ruta, 'r') as f:
       
        lineas = [l.strip() for l in f.readlines() if l.strip()]
    n = int(lineas[0])
    finca = [tuple(map(int, l.split(','))) for l in lineas[1:n+1]]
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

def roV(finca):

    ti = tm.time()
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
    tf = tm.time()
    print(f"Voraz tamaño: {n} - tiempo: {tf-ti}")
    output = f"riegoOptimo-Dinamico:{n}"
    with open(output, 'w') as salida:
        salida.write(f"{n}")
        for idx in indices_ordenados:
            salida.write(f"{idx}")
    
    return (indices_ordenados, costo)

def main(p):
    return roV(leer_finca(p))[1]
    