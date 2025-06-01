# Tarea 2: Delete Insert Edit Distance

**Asignatura:** Análisis de Algoritmos  
**Universidad:** Universidad de Concepción  
**Fecha:** Junio 2025

## Descripción

Este proyecto implementa el cálculo de distancia de edición entre dos cadenas de texto usando únicamente las operaciones **DELETE** e **INSERT** (sin REPLACE/SUBSTITUTE).

## Archivos del Proyecto

### Código Fuente
- `main.cpp` - Programa principal con casos de prueba y medición de rendimiento
- `recursive.cpp` - Implementación recursiva pura
- `memo.cpp` - Implementación recursiva con memoización
- `pdinamic.cpp` - Implementación con programación dinámica
- `pdopti.cpp` - Implementación con programación dinámica optimizada en espacio

### Archivos de Configuración
- `Makefile` - Configuración de compilación
- `README.md` - Este archivo de documentación

## Compilación y Ejecución

### Requisitos
- Compilador C++ con soporte para C++17
- Make (opcional, pero recomendado)

### Comandos Básicos

```bash
# Compilar el proyecto
make

# Compilar y ejecutar
make run

# Limpiar archivos generados
make clean

# Compilar en modo debug
make debug

# Verificar memory leaks con valgrind
make valgrind

# Mostrar información del proyecto
make info
```

### Compilación Manual
Si no tienes Make disponible:

```bash
g++ -std=c++17 -Wall -Wextra -O2 -o editdistance main.cpp recursive.cpp memo.cpp pdinamic.cpp pdopti.cpp
./editdistance
```

## Implementaciones

### 1. Recursiva Pura (`editDistanceRecursive`)
- **Enfoque:** Top-down recursivo sin optimizaciones
- **Complejidad:** O(2^(m+n)) tiempo, O(m+n) espacio
- **Uso:** Solo para cadenas pequeñas (< 10 caracteres)

### 2. Memoización (`editDistanceMemo`)
- **Enfoque:** Top-down recursivo con tabla de memoización
- **Complejidad:** O(m×n) tiempo, O(m×n) espacio
- **Uso:** Mejora significativa sobre recursión pura

### 3. Programación Dinámica (`editDistanceDP`)
- **Enfoque:** Bottom-up con tabla completa
- **Complejidad:** O(m×n) tiempo, O(m×n) espacio
- **Uso:** Más eficiente en práctica que memoización

### 4. DP Optimizada (`editDistanceDPOptimized`)
- **Enfoque:** Bottom-up con optimización de espacio
- **Complejidad:** O(m×n) tiempo, O(min(m,n)) espacio
- **Uso:** Óptima para cadenas grandes

## Casos de Prueba

El programa incluye 12 casos de prueba usando 4 cadenas:
- `""` (cadena vacía)
- `"AB"`
- `"ABC"`
- `"XYZ"`

### Casos Específicos Verificados
- `d("", "AB") = 2` (2 inserts)
- `d("AB", "") = 2` (2 deletes)
- `d("AB", "ABC") = 1` (1 insert)
- `d("ABC", "AB") = 1` (1 delete)
- `d("AB", "XYZ") = 5` (2 deletes + 3 inserts)
- `d("ABC", "XYZ") = 6` (3 deletes + 3 inserts)

## Salida del Programa

El programa genera tres secciones de output:

1. **Verificación de Casos:** Todos los 12 casos de prueba
2. **Comparación de Implementaciones:** Medición de tiempo para cada algoritmo
3. **Casos Específicos:** Verificación de casos con justificación

## Diferencias con Levenshtein Clásico

- **Levenshtein:** DELETE, INSERT, REPLACE
- **Este proyecto:** Solo DELETE, INSERT
- **Implicación:** Sin REPLACE, algunas transformaciones requieren más operaciones

## Ejemplo de Uso

```cpp
#include <iostream>
#include <string>
using namespace std;

// Usar la implementación más eficiente
int distance = editDistanceDP("hello", "world");
cout << "Distancia: " << distance << endl;
```

## Notas de Implementación

- Todas las implementaciones manejan correctamente cadenas vacías
- La versión optimizada intercambia automáticamente las cadenas si es beneficioso
- El código incluye comentarios extensivos para facilitar la comprensión
- Se incluyen mediciones de tiempo para comparar rendimiento

## Compilación para Diferentes Propósitos

```bash
# Optimización máxima para mediciones
g++ -std=c++17 -O3 -DNDEBUG -o editdistance *.cpp

# Debug con información de depuración  
g++ -std=c++17 -g -Wall -Wextra -o editdistance *.cpp

# Análisis de performance con profiling
g++ -std=c++17 -O2 -pg -o editdistance *.cpp
```