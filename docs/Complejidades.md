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

# 📊 Análisis de Complejidad Computacional - Algoritmo Voraz
## 1. Complejidad Temporal Teórica - Algoritmo Voraz
### 1.1. Descomposición del Algoritmo
El algoritmo voraz sigue la siguiente estructura:

```python
def roV(finca):
    n = len(finca)                    # O(1)
    if n == 0:                        # O(1)
        return ([], 0)                # O(1)
    
    # Orden voraz: O(n log n)
    indices_ordenados = sorted(range(n),
                               key=lambda i: (-finca[i][2] / finca[i][0], finca[i][1]))
    
    costo = calculoCostoPerm(finca, indices_ordenados)  # O(n)
    return (indices_ordenados, costo) # O(1)
```
### 1.2 Análisis Matemático Detallado
Complejidad total:

$$
T(n) = O(n \log n) + O(n) = O(n \log n)
$$

#### 1.2.1 Componentes principales:
Ordenamiento de tablones:

$$
S(n) = O(n \log n)
$$

#### 1.2.2 Cálculo de costos por permutación:
$$
C(n)=O(n) \space (funcion calculoCostoPerm)
$$
### 1.2.3 Operaciones adicionales:
$$
A(n)=O(1) \space (inicializacion y retorno)
$$

## 1.3 Función de Crecimiento
$$
f(n) = n \log n
$$

|$n$	|$f(n) = n logn $	|Ops Estim|
----|----------------|--------|
|5	|~12|	12 ops Aprox|
|8	|~24|	~24 ops|
|10	|~33|	~33 ops|
|50	|~282|	~282 ops|
|100|	~664|	~664 ops|
|1000|	~9966|	~10K ops|

## 2. Complejidad Espacial
### 2.1 Uso de Memoria por Componente
```python
def roV(finca):
    n = len(finca)                    # O(1)
    indices_ordenados = sorted(...)   # O(n) - lista ordenada
    # ... cálculo de costos
```
### 2.2 Complejidad espacial total:
$S(n) = O(n) + O(n) = O(n)$

### 2.1 Desglose detallado:
Almacenamiento de la finca: $O(n)$

Lista de índices ordenados: $O(n)$

Variables temporales en sorted(): $O(n)$

Memoria auxiliar en calculoCostoPerm: $O(n)$

### 2.3 Memoria en el Peor Caso

$M(n) = 3n + c \quad$ donde $c$ es constante

## 3. Análisis de Escalabilidad
### 3.1 Límites Prácticos de Ejecución

|n	|Tiempo Estimado	|Viabilidad|
|----|-------------------|----------|
|10	|< 1 ms	|Excelente
|100|	~1 ms|	Excelente
|1,000|	~10 ms|	Muy buena
|10,000|	~100| ms	Buena
|100,000|	~1 seg|	Aceptable
|1,000,000|	~10 seg|	Práctico para procesamiento

### 3.2 Comportamiento Asintótico
$$
\lim_{n \to \infty} \frac{n \log n}{n} = \infty \quad \text{(crecimiento super-lineal)}
$$

$$
\lim_{n \to \infty} \frac{n \log n}{n ^ 2} = 0 \quad \text{(crecimiento sub-cuadratico)}
$$

Esto confirma el crecimiento cuasi-lineal del algoritmo

## 4. Análisis de Subcomponentes
#### función sorted() (Timsort - Python):

```python
indices_ordenados = sorted(range(n),
                          key=lambda i: (-finca[i][2] / finca[i][0], finca[i][1]))
                
```

Complejidad: $O(n \log n)$

#### función calculoCostoPerm (igual que en fuerza bruta):
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
Complejidad: $O(n)$

##### función calcular_tiempos_inicio:
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

## 5. Conclusiones del Análisis
### Ventajas:
**Eficiencia temporal**: 
$$
O(n \log n)  \space \space \text{vs} \space \space O(n! \cdot n)\space \text{de fuerza bruta}
$$


**Escalabilidad excelente**: Maneja instancias grandes ($n > 1000$)

**Bajo uso de memoria:** $O(n)$ en espacio

**Tiempos de ejecución prácticos:** Sub-segundo para $n \leq 100,000$

**Implementación simple** Fácil de entender y mantener

### Limitaciones:
**No garantiza optimalidad:** Solución heurística, no óptima global

**Dependencia del criterio voraz:** La calidad de la solución depende de la función de ordenamiento

**Sensibilidad a la métrica:** El ratio $\frac{p}{ts}$ puede no capturar todas las relaciones complejas

**Posible suboptimalidad en casos específicos:** Cuando $tr$ alto afecta significativamente el costo

### Recomendaciones de Uso

>$n \leq 50$: Uso recomendado (alta calidad de solución)

>$50 < n \leq 10,000$: Uso ideal (balance perfecto calidad-eficiencia)

>$n > 10,000$: Única opción práctica para aplicaciones reales

**Validación crítica:** Para $n \leq 12$, comparar con fuerza bruta cuando sea posible

**Aplicaciones en tiempo real:** Adecuado para sistemas que requieren respuesta inmediata

### Comparación con Fuerza Bruta

|Aspecto|	Fuerza Bruta|	Algoritmo Voraz|
|-------|---------------|-------------------|
|Complejidad Temporal|	$O(n! \cdot n)$|	$O(n \log n)$|
|Complejidad Espacial|	$O(n)$	|$O(n)$|
|Optimalidad	|Garantizada	|Heurística|
|Límite Práctico|	$n \leq 12$	|$n \leq 10^6$|
|Tiempo (n=10)|	~36M ops	|~33 ops|
|Caso de Uso|	Validación	|Producción|


# 📊 Análisis de Complejidad Computacional - Programación Dinámica
## 1. Complejidad Temporal Teórica - Programación Dinámica
### 1.1. Descomposición del Algoritmo

El algoritmo de programación dinámica sigue la siguiente estructura:

```python
def roDP(finca):
    n = len(finca)                    # O(1)
    if n == 0:                        # O(1)
        return ([], 0)                # O(1)
    
    dp = {}                           # O(1)
    dp[0] = (0, -1, 0)               # O(1)
    
    for mask in range(1 << n):        # O(2^n) iteraciones
        if mask not in dp:            # O(1)
            continue
            
        costo_actual, _, tiempo_actual = dp[mask]  # O(1)
        
        for i in range(n):            # O(n) iteraciones por máscara
            if mask & (1 << i):       # O(1)
                continue
            
            nuevo_mask = mask | (1 << i)  # O(1)
            # Cálculo de penalización: O(1)
            # Actualización de dp: O(1)

    # Reconstrucción: O(n)
    return (permutacion, costo_minimo)
```

### 1.2 Análisis Matemático Detallado
**Complejidad total**:

$$
T(n) = O(2^n) \times O(n) + O(n) = O(n \cdot 2^n)
$$

#### 1.2.1 Componentes principales:
Iteración sobre todas las máscaras:
$$
M(n) = O(2^n)
$$

#### 1.2.2 Procesamiento por máscara:

$$
P(n)=O(n)\space \text{(evaluacion de todos los tablones no regados)}
$$

#### 1.2.3 Operaciones adicionales:

$$
A(n)=O(n)\space \text{(inicializacion y reconstruccion)}
$$

### 1.3 Función de Crecimiento Exponencial

$$
f(n) = n \cdot 2^n
$$

|n  |2^n|	$f(n) = n \cdot 2^n$	|Ops Estim|
|---|---|---------------------------|---------|
|5	|32	|160	|160 ops Aprox|    
|10	|1,024|	|10,240	|~10K ops|
|15	|32,768|	491,520|	~0.5M ops|
|20	|1,048,576|	20,971,520|	~21M ops|
|25	|33,554,432|	838,860,800|	~839M ops|
|30	|1,073,741,824|	32,212,254,720|	~32G ops|

## 2. Complejidad Espacial
### 2.1 Uso de Memoria por Componente
```python
def roDP(finca):
    n = len(finca)
    dp = {}                           # O(2^n) estados
    # Cada estado almacena: (costo, último_tablon, tiempo_acumulado)
```

### 2.2 Complejidad espacial total:
$$
S(n) = O(2^n) + O(n) = O(2^n)
$$

### 2.1 Desglose detallado:
**Diccionario dp:** $O(2^n)$ estados

**Cada estado:** $O(1)$ datos (3 valores)

**Memoria para reconstrucción:** $O(n)$

**Variables temporales:**  $O(1)$

### 2.3 Memoria en el Peor Caso
$$
M(n) = c \cdot 2^n + n + k \quad \text{donde $c, k$ son constantes}
$$

## . Análisis de Escalabilidad

### 3.1 Límites Prácticos de Ejecución

|n|Tiempo Estimado|	Memoria Estimada|	Viabilidad|
|-|---------------|----------------|--------------|
|10|	~10 ms	|~1 KB	|Excelente
|15|	~0.5 seg	|~32 KB	|Buena
|20|	~20 seg	|~1 MB	|Límite práctico
|25|	~10 min	|~33 MB	|Solo para validación
|30|	~5 horas	|~1 GB	|No viable en práctica

### 3.2 Comportamiento Asintótico

$$
\lim_{n \to \infty} \frac{n \cdot 2^n}{c^n} = 0 \quad \text{para cualquier constante } c > 2
$$

Esto confirma el crecimiento exponencial del algoritmo, pero más eficiente que factorial.

## 4. Análisis de Subcomponentes
Función principal DP (Dynamic Programming):
```python
for mask in range(1 << n):        # O(2^n)
    for i in range(n):            # O(n)
        # Operaciones O(1) por transición
```
Complejidad: $O(n \cdot 2^n)$

Cálculo de penalización por transición:
```python
ts_i, tr_i, p_i = finca[i]        # O(1)
tiempo_inicio = tiempo_actual     # O(1)
tiempo_fin = tiempo_inicio + tr_i # O(1)
retraso = max(0, tiempo_fin - ts_i) # O(1)
penalizacion = p_i * retraso      # O(1)
```
Complejidad: $O(1)$ por transición

Reconstrucción de solución:
```python
permutacion = []
mask_actual = mask_final
while mask_actual > 0:            # O(n) iteraciones
    _, ultimo, _ = dp[mask_actual]
    permutacion.append(ultimo)
    mask_actual ^= (1 << ultimo)
permutacion.reverse()             # O(n)
```

Complejidad: $O(n)$

## 5. Conclusiones del Análisis
### Ventajas:
- **Optimalidad garantizada:** Encuentra la solución óptima global

- **Más eficiente que fuerza bruta:** $O(n \cdot 2^n)$ vs $O(n! \cdot n)$

- **Memoización inteligente:** Evita recálculos redundantes

- **Estructura sistemática:** Exploración ordenada del espacio de búsqueda

### Limitaciones:
- **Complejidad exponencial:** $O(n \cdot 2^n)$ aún crece rápidamente

- **Uso intensivo de memoria:** $O(2^n)$ puede ser prohibitivo

- **Límite práctico bajo:** $n \leq 20-25$ en hardware típico

- **No paralelizable fácilmente:** Dependencias entre estados

### Recomendaciones de Uso
- **$n \leq 15$:** Uso recomendado (óptimo y eficiente)

- **$15 < n \leq 22$:** Uso aceptable para validación

- **$n > 22$:** Evitar por consumo de recursos

- **Casos críticos:** Cuando se requiere optimalidad garantizada

- **Benchmarking:** Como referencia para evaluar heurísticas

### 6. Comparación de las Tres Soluciones

|Aspecto	|Fuerza Bruta	|Programación Dinámica|	Algoritmo Voraz|
|--------|---------------|---------------------|----------------|
Complejidad Temporal|	$O(n! \cdot n)$|	$O(n \cdot 2^n)$	|$O(n \log n)$|
Complejidad Espacial|	$O(n)$	|$O(2^n)$	|$O(n)$
Optimalidad|	Garantizada|	Garantizada|	Heurística
Límite Práctico (n)	|$\leq 12$	|$\leq 20$|	$\leq 10^6$
Tiempo (n=10)	|~36M ops|	~10K ops|	~33 ops
Memoria (n=20)	|~80 bytes	|~1 MB	|~80 bytes
Caso de Uso|	Validación|	Optimalidad media	|Producción
Implementación|	Simple|	Moderada|	Simple|


### Resumen Comparativo
>**Fuerza Bruta:** Óptima pero solo para instancias muy pequeñas ($n \leq 12$)

>**Programación Dinámica:** Óptima y manejable para instancias medianas ($n \leq 20$)

>**Algoritmo Voraz:** No óptima pero extremadamente escalable ($n \leq 10^6$)

### Recomendación General por Tamaño
>$n \leq 12$: Fuerza Bruta (simple y óptima)

>$12 < n \leq 20$: Programación Dinámica (óptima y viable)

>$n > 20$: Algoritmo Voraz (eficiente y práctico)