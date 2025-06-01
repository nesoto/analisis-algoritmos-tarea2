#include <string>
#include <vector>
#include <algorithm>
using namespace std;

/**
 * Implementación optimizada en espacio de la distancia de edición Delete-Insert
 *
 * Observación clave: Para calcular dp[i][j] solo necesitamos:
 * - La fila anterior: dp[i-1][j-1] y dp[i-1][j]
 * - El valor anterior en la fila actual: dp[i][j-1]
 *
 * Por lo tanto, podemos usar solo 2 filas en lugar de toda la tabla.
 *
 * Parámetros:
 * - S: cadena origen
 * - T: cadena destino
 *
 * Retorna: distancia mínima de edición de S a T
 */
int editDistanceDPOptimized(const string &S, const string &T)
{
    int m = S.length();
    int n = T.length();

    // Optimización: si una cadena es mucho más larga, intercambiar roles
    // para minimizar el uso de memoria (trabajar con la más corta como "columnas")
    if (m > n)
    {
        return editDistanceDPOptimized(T, S); // Intercambiar S y T
    }

    // Ahora m <= n, usamos m+1 espacio en lugar de (m+1)*(n+1)

    // Solo necesitamos 2 filas: la anterior y la actual
    vector<int> prev(m + 1); // Fila anterior
    vector<int> curr(m + 1); // Fila actual

    // INICIALIZACIÓN DE LA PRIMERA FILA
    // prev[i] representa dp[0][i] en la implementación completa
    // Transformar cadena vacía en S[0..i-1] requiere i inserciones
    for (int i = 0; i <= m; i++)
    {
        prev[i] = i;
    }

    // PROCESAR CADA CARÁCTER DE T
    for (int j = 1; j <= n; j++)
    {
        // INICIALIZAR PRIMER ELEMENTO DE LA FILA ACTUAL
        // curr[0] representa dp[j][0] en la implementación completa
        // Transformar T[0..j-1] en cadena vacía requiere j eliminaciones
        curr[0] = j;

        // LLENAR EL RESTO DE LA FILA ACTUAL
        for (int i = 1; i <= m; i++)
        {

            if (T[j - 1] == S[i - 1])
            {
                // Los caracteres coinciden
                // curr[i] = dp[j][i] = dp[j-1][i-1] = prev[i-1]
                curr[i] = prev[i - 1];
            }
            else
            {
                // Los caracteres no coinciden
                // curr[i] = dp[j][i] = min(dp[j-1][i] + 1, dp[j][i-1] + 1)
                //                    = min(prev[i] + 1, curr[i-1] + 1)
                int deleteOption = prev[i] + 1;     // Eliminar de T
                int insertOption = curr[i - 1] + 1; // Insertar en T

                curr[i] = min(deleteOption, insertOption);
            }
        }

        // INTERCAMBIAR FILAS para la siguiente iteración
        // La fila actual se convierte en la anterior
        prev = curr;
    }

    // El resultado está en prev[m] (que era curr[m] en la última iteración)
    return prev[m];
}

/*
EXPLICACIÓN DE LA OPTIMIZACIÓN:

1. OBSERVACIÓN CLAVE:
   Para calcular dp[i][j] en la implementación estándar, solo necesitamos:
   - dp[i-1][j-1] (diagonal anterior)
   - dp[i-1][j]   (fila anterior)
   - dp[i][j-1]   (columna anterior en fila actual)

2. ESTRATEGIA:
   - Usar solo 2 vectores de tamaño m+1
   - prev[]: representa la fila anterior completa
   - curr[]: representa la fila actual que estamos calculando

3. MAPEO DE ÍNDICES:
   Implementación estándar → Implementación optimizada
   dp[i][j] → procesamos T como filas, S como columnas

   En iteración j:
   - prev[i] = dp[j-1][i] (valor de la fila anterior)
   - curr[i] = dp[j][i]   (valor que estamos calculando)

4. EJEMPLO para S="AB", T="XY":

   Inicialización:
   prev = [0, 1, 2]  // dp[0][0], dp[0][1], dp[0][2]

   j=1 (procesando T[0]='X'):
   curr[0] = 1       // dp[1][0]

   i=1: T[0]='X' != S[0]='A'
   curr[1] = min(prev[1]+1, curr[0]+1) = min(1+1, 1+1) = 2

   i=2: T[0]='X' != S[1]='B'
   curr[2] = min(prev[2]+1, curr[1]+1) = min(2+1, 2+1) = 3

   prev = curr = [1, 2, 3]

   j=2 (procesando T[1]='Y'):
   curr[0] = 2       // dp[2][0]

   i=1: T[1]='Y' != S[0]='A'
   curr[1] = min(prev[1]+1, curr[0]+1) = min(2+1, 2+1) = 3

   i=2: T[1]='Y' != S[1]='B'
   curr[2] = min(prev[2]+1, curr[1]+1) = min(3+1, 3+1) = 4

   Resultado: curr[2] = 4

5. OPTIMIZACIÓN ADICIONAL:
   - Si m > n, intercambiamos S y T
   - Esto asegura que siempre usemos min(m,n) espacio
   - El intercambio es válido porque insert/delete son operaciones complementarias

6. COMPLEJIDAD OPTIMIZADA:
   - Tiempo: O(m×n) - igual que la versión estándar
   - Espacio: O(min(m,n)) - gran mejora desde O(m×n)

7. VENTAJAS:
   - Mucho menor uso de memoria para cadenas grandes
   - Mejor cache locality (acceso secuencial a vectores pequeños)
   - Permite procesar cadenas más grandes en memoria limitada
*/