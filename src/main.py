import sys 
import os 
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import roFB
import roV
import roD

import fileChooser as fc

modified_route = None

def leer_finca(route):
    ruta = route
    with open(ruta, 'r') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]
    n = int(lineas[0])
    finca = [tuple(map(int, l.split(','))) for l in lineas[1:n+1]]
    
    return finca
def exit():
    print("Adios")
    return False

def main(r='src/finca.txt', n=None):
    global modified_route
    route = modified_route if (modified_route != None) else r
    route = os.path.abspath(modified_route) if modified_route != None else os.path.abspath(r)
    if n == None:
        print("          Riego Optimo")
        text = ["Soluciones:", " 1 - Fuerza bruta", " 2 - Programamcion Voraz", " 3 - Programacion Dinamica", " 4 - Comparacion", " 5 - Especificar archivo (si no se hace toma uno por defecto)", "SALIR : digite SALIR"]
        for t in text:
            print(f"\n{t}")
        opt = " "
        while type(opt) != int or opt == 0 or opt > 5 :
            
            try: 
                opt = input("\nDigite el numero de su eleccion  y presione ENTER:")
                if opt == "SALIR":
                    return False
                opt = int(opt)

            except ValueError:
                print("Eleccion no disponible 🙄")
            
            except TypeError:
                print("Eleccion no disponible 🙄")
            
            if type(opt) != int:
                print("Eleccion no disponible 🙄")
            
            elif opt == 5:
                modified_route = fc.select_file()
                print(f"source : {modified_route}")
            elif opt > 5:
                print("No tenemos tantas opciones")
                opt = 0
        
    else: 
        opt = n
        
    if opt == 1 or opt == 4:
        print("FB")
        # === BLOQUE FUERZA BRUTA ===
        finca = leer_finca(route)
        print(f"source : {route}")
        tiempo_i = time.time()
        mejor_permutacion, mejor_costo = roFB.roFB(finca)
        tiempo_f = time.time()

        print("=======================================================================")
        print("RESULTADO ÓPTIMO")
        print("=======================================================================")
        print("Tiempo de ejecución:", tiempo_f - tiempo_i)
        
        print(mejor_costo)
        '''
        for idx in mejor_permutacion:
            print(idx)
            '''
        input("Enter para continuar")

    if opt == 2 or opt == 4:
        print("V")
        # === BLOQUE VORAZ ===
        finca = leer_finca(route)
        print(f"source : {route}")
        tiempo_i_v = time.time()
        perm_v, costo_v = roV.roV(finca)
        tiempo_f_v = time.time()

        print("\n=======================================================================")
        print("RESULTADO VORAZ")
        print("=======================================================================")
        print("Tiempo de ejecución:", tiempo_f_v - tiempo_i_v)
        print(costo_v)
        '''
        for idx in perm_v:
            print(idx)
            '''
        input("Enter para continuar")
    
    if opt == 3 or opt == 4:
        print("D")
        # === BLOQUE DINAMICO ===
        finca = leer_finca(route)
        print(f"source : {route}")
        tiempo_i_d = time.time()
        perm_d, costo_d = roD.roDP(finca)
        print("returns")
        tiempo_f_d = time.time()

        print("\n=======================================================================")
        print("RESULTADO DINAMICO")
        print("=======================================================================")
        print("Tiempo de ejecución:", tiempo_f_d - tiempo_i_d)
        print(costo_d)
        '''
        for idx in perm_d:
            print(idx)
            '''
        input("Enter para continuar")

if __name__ == "__main__":
    
    while True:
        running = main()
        if running == False:
            break
    