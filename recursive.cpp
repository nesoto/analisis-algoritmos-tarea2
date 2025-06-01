#include <string>
#include <algorithm>
using namespace std;

/**
 * Implementación recursiva pura de la distancia de edición Delete-Insert
 *
 * Parámetros:
 * - S: cadena origen
 * - T: cadena destino
 * - i: índice actual en S
 * - j: índice actual en T
 *
 * Retorna: distancia mínima de edición de S[i..] a T[j..]
 */
int editDistanceRecursive(const string &S, const string &T, int i, int j)
{
    // Caso base 1: Si llegamos al final de S, necesitamos insertar todos los caracteres restantes de T
    if (i == S.length())
    {
        return T.length() - j; // Insertar todos los caracteres restantes de T
    }

    // Caso base 2: Si llegamos al final de T, necesitamos eliminar todos los caracteres restantes de S
    if (j == T.length())
    {
        return S.length() - i; // Eliminar todos los caracteres restantes de S
    }

    // Caso recursivo: Comparar caracteres actuales
    if (S[i] == T[j])
    {
        // Los caracteres coinciden, avanzamos en ambas cadenas sin costo adicional
        return editDistanceRecursive(S, T, i + 1, j + 1);
    }
    else
    {
        // Los caracteres no coinciden, tenemos dos opciones:

        // Opción 1: Eliminar carácter actual de S (avanzar en S)
        int deleteOption = 1 + editDistanceRecursive(S, T, i + 1, j);

        // Opción 2: Insertar carácter de T en S (avanzar en T)
        int insertOption = 1 + editDistanceRecursive(S, T, i, j + 1);

        // Retornar la opción con menor costo
        return min(deleteOption, insertOption);
    }
}

/*
EXPLICACIÓN DEL ALGORITMO:

1. CASOS BASE:
   - Si i == len(S): Hemos procesado toda S, solo queda insertar el resto de T
   - Si j == len(T): Hemos procesado toda T, solo queda eliminar el resto de S

2. CASO RECURSIVO:
   - Si S[i] == T[j]: Los caracteres coinciden, avanzamos gratis en ambas
   - Si S[i] != T[j]: Tenemos dos opciones:
     * DELETE: Eliminar S[i] y continuar con S[i+1] vs T[j]
     * INSERT: "Insertar" T[j] y continuar con S[i] vs T[j+1]

3. COMPLEJIDAD:
   - Tiempo: O(2^(m+n)) en el peor caso - EXPONENCIAL
   - Espacio: O(m+n) por la pila de recursión
   - Problema: Muchos subproblemas se resuelven múltiples veces

4. EJEMPLO DE EJECUCIÓN:
   editDistanceRecursive("AB", "AC", 0, 0)
   ├─ S[0]='A' == T[0]='A' → editDistanceRecursive("AB", "AC", 1, 1)
      ├─ S[1]='B' != T[1]='C'
         ├─ DELETE: 1 + editDistanceRecursive("AB", "AC", 2, 1)
         │  └─ i==2, j==1 → return 1 (insertar 'C')
         │  └─ Total: 1 + 1 = 2
         └─ INSERT: 1 + editDistanceRecursive("AB", "AC", 1, 2)
            └─ i==1, j==2 → return 1 (eliminar 'B')
            └─ Total: 1 + 1 = 2
   → min(2, 2) = 2
*/