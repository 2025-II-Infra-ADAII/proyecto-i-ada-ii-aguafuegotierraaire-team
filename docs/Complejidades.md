# 📊 Análisis de Complejidad Computacional

## 1. Complejidad Temporal Teórica - Fuerza Bruta

### 1.1. Descomposición del Algoritmo

El algoritmo de fuerza bruta sigue la siguiente estructura:

```python
def roFB(finca):
    n = len(finca)                    # O(1)
    indices = list(range(n))          # O(n)
    
    for permutacion in permutations(indices):  # O(n!) iteraciones
        costo = calculoCostoPerm(finca, permutacion)  # O(n)
        if costo < mejor_costo:       # O(1)
            mejor_costo = costo       # O(1)
            mejor_permutacion = permutacion  # O(n)
```

### 1.2 Análisis Matemático Detallado

Complejidad total:

$T(n) = O(n!) \times O(n) + O(n) = O(n! \cdot n)$

#### 1.2.1 Componentes principales:
Generación de permutaciones:

$P(n) = n! \Rightarrow O(n!)$
    
#### 1.2.2 Cálculo de costos por permutación:
$$
C(n) = O(n) \quad \text{(incluye calcular\_tiempos\_inicio y calculoCostoPerm)}
$$
    
#### 1.2.3 Operaciones adicionales:
$$
    A(n) = O(n) \quad \text{(inicialización y actualización)}
$$

### 1.3 Función de Crecimiento Exponencial

$f(n) = n! \cdot n$

| n  	| n!                	| f(n) = n! x n      	| Ops Estim     	|
|----	|-------------------	|--------------------	|---------------	|
| 5  	| 120               	| 600                	| 600 ops Aprox 	|
| 8  	| 40320             	| 322,560            	| ~0.3M ops     	|
| 10 	| 3,628,800         	| 36,288,000         	| ~36M ops      	|
| 12 	| 479,001,600       	| 5,748,019,200      	| ~5.7G ops     	|
| 15 	| 1,307,674,368,000 	| 19,615,115,520,000 	| ~19.6T ops    	|

### 2. Complejidad Espacial

#### 2.1 Uso de Memoria por Componente
```python
def roFB(finca):
    n = len(finca)
    indices = list(range(n))          # O(n)
    mejor_permutacion = None          # O(n) en el peor caso
    
    for permutacion in permutations(indices):  # O(n) por permutación
        tiempos_inicio = {}           # O(n) - diccionario temporal
        # ... cálculo de costos
```

#### 2.2 Complejidad espacial total:
$S(n) = O(n) + O(n) + O(n) = O(n)$

##### 2.1 Desglose detallado:

Almacenamiento de la finca: $O(n)$
- Lista de índices: $O(n)$
- Mejor permutación almacenada: $O(n)$
- Variables temporales por iteración: $O(n)$
- tiempos_inicio: diccionario con $n$ entradas
- permutacion: tupla de $n$ elementos


#### 2.3 Memoria en el Peor Caso

$M(n) = 4n + c \quad$

donde $c$ es constante

### 3. Análisis de Escalabilidad


#### 3.1 Límites Prácticos de Ejecución

| n  	| Tiempo Estimado 	| Viabilidad                           	|
|----	|-----------------	|--------------------------------------	|
| 5  	| 0.6 ms          	| Excelente                            	|
| 8  	| 0.3 seg         	| Buena                                	|
| 10 	| 20-25 seg       	| Aceptable para pruebas               	|
| 12 	| 1.6 horas       	| Límite práctico                      	|
| 15 	| No testeado     	| No viable por su tiempo de ejecución 	|

#### 3.2 Comportamiento Asintótico

$$
\lim_{n \to \infty} \frac{n! \cdot n}{c^n} = \infty \quad \text{para cualquier constante } c > 1
$$

Esto confirma el crecimiento $super-exponencial$ del algoritmo.


### 4. Análisis de Subcomponentes

#### función calcular_tiempos_inicio:
```python
def calcular_tiempos_inicio(finca, permutacion):
    tiempos = {}
    tiempo_actual = 0                 # O(1)
    
    for tablon in permutacion:        # O(n) iteraciones
        tiempos[tablon] = tiempo_actual  # O(1)
        tr = finca[tablon][1]         # O(1)
        tiempo_actual += tr           # O(1)
    
    return tiempos
```

Complejidad: $O(n)$

#### función calculoCostoPerm
```python
def calculoCostoPerm(finca, permutacion):
    tiempos_inicio = calcular_tiempos_inicio(finca, permutacion)  # O(n)
    costo_total = 0                      # O(1)
    
    for tablon in range(len(finca)):     # O(n) iteraciones
        ts, tr, p = finca[tablon]        # O(1)
        t_inicio = tiempos_inicio[tablon] # O(1)
        t_fin_riego = t_inicio + tr      # O(1)
        penalizacion = p * max(0, t_fin_riego - ts)  # O(1)
        costo_total += penalizacion      # O(1)
    
    return costo_total
```
Complejidad $O(n)$

### 5. Conclusiones del Análisis

#### Ventajas
- Optimalidad garantizada: Explora todo el espacio de soluciones
- Simplicidad conceptual: Fácil de implementar y entender
- Precisión absoluta: Encuentra la solución óptima global


#### Limitaciones

- Complejidad factorial: $O(n! \cdot n)$ crece extremadamente rápido
- Impráctico para $n > 12$: Tiempos de ejecución prohibitivos
- Uso intensivo de CPU: Aunque la memoria es lineal, el procesamiento es masivo

#### Recomendaciones de Uso

- $n \leq 8$: Uso recomendado
- $9 \leq n \leq 12$: Solo para validación y pruebas
- $n \geq 13$: Evitar completamente en aplicaciones 
