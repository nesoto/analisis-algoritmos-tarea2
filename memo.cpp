#include <string>
#include <vector>
#include <algorithm>
using namespace std;

/**
 * Implementación recursiva con memoización de la distancia de edición Delete-Insert
 *
 * La memoización evita recalcular los mismos subproblemas múltiples veces
 *
 * Parámetros:
 * - S: cadena origen
 * - T: cadena destino
 * - i: índice actual en S
 * - j: índice actual en T
 * - memo: tabla de memoización (inicializada con -1)
 *
 * Retorna: distancia mínima de edición de S[i..] a T[j..]
 */
int editDistanceMemo(const string &S, const string &T, int i, int j, vector<vector<int>> &memo)
{
    // Verificar si ya calculamos este subproblema
    if (memo[i][j] != -1)
    {
        return memo[i][j]; // Retornar valor ya calculado
    }

    int result;

    // Caso base 1: Si llegamos al final de S, insertar todos los caracteres restantes de T
    if (i == S.length())
    {
        result = T.length() - j;
    }
    // Caso base 2: Si llegamos al final de T, eliminar todos los caracteres restantes de S
    else if (j == T.length())
    {
        result = S.length() - i;
    }
    // Caso recursivo: Comparar caracteres actuales
    else if (S[i] == T[j])
    {
        // Los caracteres coinciden, avanzamos en ambas cadenas sin costo
        result = editDistanceMemo(S, T, i + 1, j + 1, memo);
    }
    else
    {
        // Los caracteres no coinciden, evaluamos ambas opciones

        // Opción 1: Eliminar carácter actual de S
        int deleteOption = 1 + editDistanceMemo(S, T, i + 1, j, memo);

        // Opción 2: Insertar carácter de T en S
        int insertOption = 1 + editDistanceMemo(S, T, i, j + 1, memo);

        // Tomar la opción con menor costo
        result = min(deleteOption, insertOption);
    }

    // Guardar el resultado en la tabla de memoización
    memo[i][j] = result;
    return result;
}

/*
EXPLICACIÓN DE LA MEMOIZACIÓN:

1. TABLA MEMO:
   - Dimensiones: (len(S)+1) x (len(T)+1)
   - memo[i][j] = distancia de S[i..] a T[j..]
   - Inicializada con -1 (indica "no calculado")

2. FUNCIONAMIENTO:
   - Antes de calcular: verificar si memo[i][j] != -1
   - Si ya está calculado: retornar memo[i][j]
   - Si no: calcular normalmente y guardar en memo[i][j]

3. VENTAJAS:
   - Evita recálculos de subproblemas
   - Tiempo: O(m×n) en lugar de O(2^(m+n))
   - Cada subproblema se resuelve exactamente una vez

4. COMPLEJIDAD MEJORADA:
   - Tiempo: O(m×n) donde m=len(S), n=len(T)
   - Espacio: O(m×n) para la tabla + O(m+n) pila de recursión

5. EJEMPLO DE MEMOIZACIÓN:
   Para editDistanceMemo("AB", "XY", 0, 0, memo):

   Llamadas y almacenamiento en memo:
   memo[0][0] = ? → calcular
   ├─ memo[1][0] = ? → calcular → memo[1][0] = 2
   ├─ memo[0][1] = ? → calcular → memo[0][1] = 3
   └─ memo[0][0] = min(1+2, 1+3) = 3

   Si se vuelve a llamar editDistanceMemo("AB", "XY", 0, 0, memo):
   → Retorna inmediatamente memo[0][0] = 3 (ya calculado)

6. PATRÓN TOP-DOWN:
   - Empezamos desde el problema original
   - Recursivamente dividimos en subproblemas
   - Memorizamos resultados para evitar recálculos
*/