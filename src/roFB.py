# Codiguito para Solución por fuerza brurisisisisisima
from itertools import permutations
import time

def leer_finca():
    ruta = 'src/finca.txt'
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


        
def mostrar_detalle_solucion(finca, permutacion, costo):
    
    print("=" * 70)
    print("SOLUCIÓN POR FUERZA BRUTA")
    print("=" * 70)
    
    print(f"\nFinca con {len(finca)} tablones")
    print("\n┌────────┬────┬────┬───────────┐")
    print("│ Tablón │ TS │ TR │ Prioridad │")
    print("├────────┼────┼────┼───────────┤")
    for i, (ts, tr, p) in enumerate(finca):
        print(f"│   {i:2}   │ {ts:2} │ {tr:2} │     {p}     │")
    print("└────────┴────┴────┴───────────┘")
    
    print(f"\n{'=' * 70}")
    print("RESULTADO ÓPTIMO")
    print("=" * 70)
    print(f"Orden de riego: {permutacion}")
    print(f"Costo mínimo: {costo}")
    
    tiempos = calcular_tiempos_inicio(finca, permutacion)
    
    print("\n┌────────┬────────┬─────┬────┬─────────┬────────┬─────────────┐")
    print("│ Tablón │ Inicio │ Fin │ TS │ Retraso │ Prior. │ Penalización│")
    print("├────────┼────────┼─────┼────┼─────────┼────────┼─────────────┤")
    
    for idx in permutacion:
        ts, tr, p = finca[idx]
        t_inicio = tiempos[idx]
        t_fin = t_inicio + tr
        retraso = max(0, t_fin - ts)
        penal = p * retraso
        
        print(f"│   {idx:2}   │   {t_inicio:2}   │ {t_fin:2}  │ {ts:2} │   {retraso:2}    │   {p}    │     {penal:3}     │")
    
    print("└────────┴────────┴─────┴────┴─────────┴────────┴─────────────┘")
    print(f"\nCosto total: {costo}")


if __name__ == "__main__":
    finca = leer_finca()

    tiempo_ini_sol = time.time()
    mejor_permutacion, mejor_costo = roFB(finca)

    tiempo_fin_sol = time.time()
    tiempo_total = tiempo_fin_sol - tiempo_ini_sol

    print("Mejor permutación:", mejor_permutacion)
    print("Mejor costo:", mejor_costo)
    print("Tiempo total de solución:", tiempo_total)

    mostrar_detalle_solucion(finca, mejor_permutacion, mejor_costo)