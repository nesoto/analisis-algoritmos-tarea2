#include <string>
#include <vector>
#include <algorithm>
using namespace std;

/**
 * Implementación con Programación Dinámica (Bottom-Up) de la distancia de edición Delete-Insert
 *
 * Construye una tabla DP donde dp[i][j] representa la distancia mínima
 * para transformar S[0..i-1] en T[0..j-1]
 *
 * Parámetros:
 * - S: cadena origen
 * - T: cadena destino
 *
 * Retorna: distancia mínima de edición de S a T
 */
int editDistanceDP(const string &S, const string &T)
{
    int m = S.length();
    int n = T.length();

    // Crear tabla DP de (m+1) x (n+1)
    // dp[i][j] = distancia para transformar S[0..i-1] en T[0..j-1]
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));

    // INICIALIZACIÓN DE CASOS BASE

    // dp[i][0]: transformar S[0..i-1] en cadena vacía
    // Necesitamos eliminar todos los i caracteres de S
    for (int i = 0; i <= m; i++)
    {
        dp[i][0] = i; // i eliminaciones
    }

    // dp[0][j]: transformar cadena vacía en T[0..j-1]
    // Necesitamos insertar todos los j caracteres de T
    for (int j = 0; j <= n; j++)
    {
        dp[0][j] = j; // j inserciones
    }

    // LLENAR LA TABLA DP
    for (int i = 1; i <= m; i++)
    {
        for (int j = 1; j <= n; j++)
        {

            if (S[i - 1] == T[j - 1])
            {
                // Los caracteres coinciden, no hay costo adicional
                dp[i][j] = dp[i - 1][j - 1];
            }
            else
            {
                // Los caracteres no coinciden, elegir la mejor opción:

                // Opción 1: Eliminar S[i-1] (viene de dp[i-1][j])
                int deleteOption = dp[i - 1][j] + 1;

                // Opción 2: Insertar T[j-1] (viene de dp[i][j-1])
                int insertOption = dp[i][j - 1] + 1;

                // Tomar la opción con menor costo
                dp[i][j] = min(deleteOption, insertOption);
            }
        }
    }

    // El resultado está en dp[m][n]
    return dp[m][n];
}

/*
EXPLICACIÓN DE LA PROGRAMACIÓN DINÁMICA:

1. TABLA DP:
   - Dimensiones: (m+1) x (n+1)
   - dp[i][j] = distancia para transformar S[0..i-1] en T[0..j-1]
   - Índices desde 0 para incluir casos base con cadenas vacías

2. INICIALIZACIÓN:
   - dp[i][0] = i (eliminar todos los caracteres de S[0..i-1])
   - dp[0][j] = j (insertar todos los caracteres de T[0..j-1])

3. RECURRENCIA:
   Si S[i-1] == T[j-1]:
       dp[i][j] = dp[i-1][j-1]  (sin costo)
   Sino:
       dp[i][j] = min(
           dp[i-1][j] + 1,    // eliminar S[i-1]
           dp[i][j-1] + 1     // insertar T[j-1]
       )

4. EJEMPLO PASO A PASO para S="AB", T="XY":

   Inicialización:
       ""  X   Y
   ""   0   1   2
   A    1
   B    2

   Llenar tabla:
   i=1, j=1: S[0]='A' != T[0]='X'
   dp[1][1] = min(dp[0][1]+1, dp[1][0]+1) = min(1+1, 1+1) = 2

   i=1, j=2: S[0]='A' != T[1]='Y'
   dp[1][2] = min(dp[0][2]+1, dp[1][1]+1) = min(2+1, 2+1) = 3

   i=2, j=1: S[1]='B' != T[0]='X'
   dp[2][1] = min(dp[1][1]+1, dp[2][0]+1) = min(2+1, 2+1) = 3

   i=2, j=2: S[1]='B' != T[1]='Y'
   dp[2][2] = min(dp[1][2]+1, dp[2][1]+1) = min(3+1, 3+1) = 4

   Tabla final:
       ""  X   Y
   ""   0   1   2
   A    1   2   3
   B    2   3   4

   Resultado: dp[2][2] = 4

5. COMPLEJIDAD:
   - Tiempo: O(m×n) - un solo recorrido de la tabla
   - Espacio: O(m×n) - tabla completa
   - Más eficiente que recursión con memoización en práctica

6. VENTAJAS DEL ENFOQUE BOTTOM-UP:
   - No hay overhead de recursión
   - Mejor localidad de memoria
   - Más fácil de optimizar el uso de espacio
*/