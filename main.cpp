#include <iostream>
#include <string>
#include <vector>
#include <chrono>
using namespace std;
using namespace std::chrono;

// Declaraciones de funciones de cada implementación
int editDistanceRecursive(const string &S, const string &T, int i, int j);
int editDistanceMemo(const string &S, const string &T, int i, int j, vector<vector<int>> &memo);
int editDistanceDP(const string &S, const string &T);
int editDistanceDPOptimized(const string &S, const string &T);

// Función auxiliar para memoización
int editDistanceMemoWrapper(const string &S, const string &T)
{
    vector<vector<int>> memo(S.length() + 1, vector<int>(T.length() + 1, -1));
    return editDistanceMemo(S, T, 0, 0, memo);
}

// Función para medir tiempo de ejecución
template <typename Func>
void measureTime(const string &name, Func func, const string &S, const string &T)
{
    auto start = high_resolution_clock::now();
    int result = func(S, T);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);

    cout << name << "(\"" << S << "\", \"" << T << "\") = " << result
         << " [Tiempo: " << duration.count() << " μs]" << endl;
}

int main()
{
    cout << "=== TAREA 2: DELETE-INSERT EDIT DISTANCE ===" << endl;
    cout << "Casos de Prueba con las 4 cadenas seleccionadas\n"
         << endl;

    // Cadenas de prueba
    vector<string> strings = {"", "ABC", "HELLO", "WORLD"};

    cout << "1. VERIFICACIÓN DE CASOS DE PRUEBA:" << endl;
    cout << "-----------------------------------" << endl;

    // Probar todos los casos con implementación recursiva (más simple para verificar)
    for (int i = 0; i < strings.size(); i++)
    {
        for (int j = 0; j < strings.size(); j++)
        {
            if (i != j)
            { // Excluir casos idénticos
                int result = editDistanceRecursive(strings[i], strings[j], 0, 0);
                cout << "d(\"" << strings[i] << "\", \"" << strings[j] << "\") = " << result << endl;
            }
        }
    }

    cout << "\n2. COMPARACIÓN DE IMPLEMENTACIONES:" << endl;
    cout << "-----------------------------------" << endl;

    // Casos de prueba para comparar implementaciones
    vector<pair<string, string>> testCases = {
        {"", "ABC"},
        {"ABC", "HELLO"},
        {"HELLO", "WORLD"},
        {"ABC", "WORLD"}};

    for (auto &test : testCases)
    {
        cout << "\nCaso: \"" << test.first << "\" -> \"" << test.second << "\"" << endl;

        // Solo medir implementaciones eficientes para casos grandes
        if (test.first.length() <= 10 && test.second.length() <= 10)
        {
            measureTime("Recursivo     ", [](const string &s, const string &t)
                        { return editDistanceRecursive(s, t, 0, 0); }, test.first, test.second);
        }

        measureTime("Memoización   ", editDistanceMemoWrapper, test.first, test.second);
        measureTime("Prog.Dinámica ", editDistanceDP, test.first, test.second);
        measureTime("DP Optimizada ", editDistanceDPOptimized, test.first, test.second);
    }

    cout << "\n3. CASOS DE PRUEBA ESPECÍFICOS:" << endl;
    cout << "-------------------------------" << endl;

    // Verificar casos específicos mencionados en la justificación
    struct TestCase
    {
        string s, t;
        int expected;
        string justification;
    };

    vector<TestCase> specificTests = {
        {"", "ABC", 3, "3 inserts: 'A', 'B', 'C'"},
        {"ABC", "", 3, "3 deletes: 'A', 'B', 'C'"},
        {"", "HELLO", 5, "5 inserts: 'H', 'E', 'L', 'L', 'O'"},
        {"HELLO", "", 5, "5 deletes: 'H', 'E', 'L', 'L', 'O'"},
        {"", "WORLD", 5, "5 inserts: 'W', 'O', 'R', 'L', 'D'"},
        {"WORLD", "", 5, "5 deletes: 'W', 'O', 'R', 'L', 'D'"},
        {"ABC", "HELLO", 8, "3 deletes + 5 inserts"},
        {"HELLO", "ABC", 8, "5 deletes + 3 inserts"},
        {"ABC", "WORLD", 8, "3 deletes + 5 inserts"},
        {"WORLD", "ABC", 8, "5 deletes + 3 inserts"},
        {"HELLO", "WORLD", 8, "delete 'H','E','L','O', insert 'W','O','R','D' (optimizado)"},
        {"WORLD", "HELLO", 8, "delete 'W','O','R','D', insert 'H','E','L','O' (optimizado)"}};

    bool allCorrect = true;
    for (auto &test : specificTests)
    {
        int result = editDistanceDP(test.s, test.t);
        bool correct = (result == test.expected);
        allCorrect &= correct;

        cout << "d(\"" << test.s << "\", \"" << test.t << "\") = " << result
             << " [Esperado: " << test.expected << "] "
             << (correct ? "✓" : "✗") << " - " << test.justification << endl;
    }

    cout << "\nResultado: " << (allCorrect ? "Todos los casos CORRECTOS ✓" : "Hay casos INCORRECTOS ✗") << endl;

    return 0;
}