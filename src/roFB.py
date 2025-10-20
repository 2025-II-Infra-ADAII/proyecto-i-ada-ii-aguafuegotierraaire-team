# Codiguito para Solución por fuerza brurisisisisisima
from itertools import permutations

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

def main(p):
    return roFB(leer_finca(p))[1]
