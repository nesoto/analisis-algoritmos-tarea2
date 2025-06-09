#!/usr/bin/env python3
"""
Versión directa del experimento sin archivos intermedios
"""

import subprocess
import os
import json
import time

def compile_test_programs():
    """Compila programas individuales para cada algoritmo"""
    print("Compilando programas de prueba...\n")
    
    algorithms = {
        'recursive': 'editDistanceRecursive(S, T, 0, 0)',
        'memo': 'editDistanceMemoWrapper(S, T)',
        'dp': 'editDistanceDP(S, T)',
        'dpopt': 'editDistanceDPOptimized(S, T)'
    }
    
    base_code = """
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
using namespace std;
using namespace std::chrono;

// Declaraciones
int editDistanceRecursive(const string &S, const string &T, int i, int j);
int editDistanceMemo(const string &S, const string &T, int i, int j, vector<vector<int>> &memo);
int editDistanceDP(const string &S, const string &T);
int editDistanceDPOptimized(const string &S, const string &T);

int editDistanceMemoWrapper(const string &S, const string &T) {{
    vector<vector<int>> memo(S.length() + 1, vector<int>(T.length() + 1, -1));
    return editDistanceMemo(S, T, 0, 0, memo);
}}

int main(int argc, char* argv[]) {{
    if (argc != 3) {{
        cerr << "Uso: " << argv[0] << " <string1> <string2>" << endl;
        return 1;
    }}
    
    string S = argv[1];
    string T = argv[2];
    
    auto start = high_resolution_clock::now();
    int result = {ALGO_CALL};
    auto end = high_resolution_clock::now();
    
    auto duration = duration_cast<microseconds>(end - start).count();
    
    cout << result << "," << duration << endl;
    
    return 0;
}}
"""
    
    success_count = 0
    
    for algo_name, algo_call in algorithms.items():
        # Crear código específico
        code = base_code.replace('{ALGO_CALL}', algo_call)
        
        # Guardar archivo
        filename = f'test_{algo_name}.cpp'
        with open(filename, 'w') as f:
            f.write(code)
        
        # Compilar
        exe_name = f'test_{algo_name}'
        cmd = f'g++ -std=c++17 -O2 -o {exe_name} {filename} ../recursive.cpp ../memo.cpp ../pdinamic.cpp ../dpopti.cpp'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {algo_name} compilado exitosamente")
            success_count += 1
        else:
            print(f"✗ Error compilando {algo_name}:")
            print(result.stderr[:200])
    
    return success_count == len(algorithms)

def load_texts():
    """Carga los textos de los archivos"""
    texts = {}
    text_files = ['text1.txt', 'text2.txt', 'text3.txt', 'text4.txt']
    
    for filename in text_files:
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
            texts[filename] = content
            print(f"✓ Cargado {filename}: {len(content)} caracteres")
        except:
            print(f"✗ Error cargando {filename}")
            return None
    
    return texts

def run_single_test(algo, text1, text2, repeat=3):
    """Ejecuta un test individual"""
    exe_name = f'./test_{algo}'
    
    times = []
    distance = -1
    
    for _ in range(repeat):
        try:
            # Ejecutar pasando los textos como argumentos
            # Nota: Para textos largos, esto puede fallar por límite de argumentos
            cmd = [exe_name, text1, text2]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and ',' in result.stdout:
                parts = result.stdout.strip().split(',')
                distance = int(parts[0])
                time_us = int(parts[1])
                times.append(time_us)
        except subprocess.TimeoutExpired:
            print(f"    Timeout en {algo}")
            return -1, -1
        except Exception as e:
            print(f"    Error en {algo}: {e}")
            return -1, -1
    
    if times:
        avg_time = sum(times) / len(times)
        return distance, avg_time
    
    return -1, -1

def main():
    os.chdir('/Users/nico/Desktop/Universidad/Analisis/analisis-algoritmos-tarea2/experimental')
    
    print("=== EXPERIMENTO DIRECTO ===\n")
    
    # 1. Compilar programas
    if not compile_test_programs():
        print("\nError en la compilación. Abortando.")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 2. Cargar textos
    texts = load_texts()
    if not texts:
        print("\nError cargando textos. Abortando.")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 3. Ejecutar experimentos
    print("Ejecutando experimentos...\n")
    
    results = []
    text_names = list(texts.keys())
    
    # Para textos muy largos, usar solo una muestra
    MAX_LEN = 1000  # Límite para evitar problemas con argumentos
    
    for i, file1 in enumerate(text_names):
        for j, file2 in enumerate(text_names):
            if i != j:
                text1 = texts[file1][:MAX_LEN]
                text2 = texts[file2][:MAX_LEN]
                
                print(f"{file1} -> {file2} (usando primeros {MAX_LEN} chars):")
                
                # Determinar algoritmos a usar
                if len(text1) < 100 and len(text2) < 100:
                    algos = ['recursive', 'memo', 'dp', 'dpopt']
                else:
                    algos = ['memo', 'dp', 'dpopt']
                
                for algo in algos:
                    print(f"  {algo}: ", end='', flush=True)
                    
                    distance, time_us = run_single_test(algo, text1, text2)
                    
                    if distance != -1:
                        time_ms = time_us / 1000
                        print(f"d={distance}, t={time_ms:.2f}ms")
                        
                        results.append({
                            'from': file1,
                            'to': file2,
                            'algorithm': algo,
                            'distance': distance,
                            'time_ms': time_ms,
                            'text1_len': len(text1),
                            'text2_len': len(text2)
                        })
                    else:
                        print("ERROR")
                
                print()
    
    # 4. Guardar resultados
    with open('results_direct.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Resultados guardados en results_direct.json")
    
    # 5. Mostrar resumen
    print("\n=== RESUMEN ===")
    
    if results:
        # Mostrar algunas distancias
        print("\nAlgunas distancias calculadas:")
        for r in results[:5]:
            print(f"{r['from']} -> {r['to']}: d={r['distance']} ({r['algorithm']})")
        
        # Promedios por algoritmo
        print("\nTiempos promedio por algoritmo:")
        algo_times = {}
        for r in results:
            algo = r['algorithm']
            if algo not in algo_times:
                algo_times[algo] = []
            algo_times[algo].append(r['time_ms'])
        
        for algo, times in algo_times.items():
            avg = sum(times) / len(times)
            print(f"  {algo}: {avg:.2f}ms")
    else:
        print("\nNo se obtuvieron resultados válidos.")

if __name__ == "__main__":
    main()
