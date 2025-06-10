#!/usr/bin/env python3
"""
Experimento simple para medir tiempos de los algoritmos
"""

import subprocess
import matplotlib.pyplot as plt
import time

# Primero crear los textos de prueba
def crear_textos():
    """Crea 4 textos de diferentes tamaños"""
    print("Creando archivos de texto...")
    
    # text1: ~20 palabras
    text1 = "It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife"
    
    # text2: ~75 palabras (repetir text1 unas veces)
    text2 = text1 + " " + text1 + " " + text1 + " However little known the feelings or views of such a man may be"
    
    # text3: ~500 palabras (un párrafo más largo)
    text3 = (text1 + " ") * 20 + "This truth is so well fixed in the minds of the surrounding families"
    
    # text4: ~1500 palabras (capítulo pequeño)
    text4 = (text1 + " ") * 65
    
    # Guardar archivos
    with open('text1.txt', 'w') as f:
        f.write(text1)
    with open('text2.txt', 'w') as f:
        f.write(text2)
    with open('text3.txt', 'w') as f:
        f.write(text3)
    with open('text4.txt', 'w') as f:
        f.write(text4)
    
    print(f"text1.txt: {len(text1.split())} palabras")
    print(f"text2.txt: {len(text2.split())} palabras")
    print(f"text3.txt: {len(text3.split())} palabras")
    print(f"text4.txt: {len(text4.split())} palabras")

# Compilar el programa de prueba
def compilar():
    """Compila el programa con todos los algoritmos"""
    print("\nCompilando programa...")
    cmd = "g++ -std=c++17 -O2 -o test_program test_program.cpp ../recursive.cpp ../memo.cpp ../pdinamic.cpp ../dpopti.cpp"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode == 0:
        print("Compilación exitosa!")
    else:
        print("Error al compilar:", result.stderr.decode())
        exit(1)

# Crear el programa de prueba
def crear_programa_prueba():
    """Crea un programa C++ simple para probar"""
    codigo = """
#include <iostream>
#include <fstream>
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

int editDistanceMemoWrapper(const string &S, const string &T) {
    vector<vector<int>> memo(S.length() + 1, vector<int>(T.length() + 1, -1));
    return editDistanceMemo(S, T, 0, 0, memo);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Uso: " << argv[0] << " <file1> <file2> <algoritmo>" << endl;
        return 1;
    }
    
    // Leer archivos
    ifstream f1(argv[1]), f2(argv[2]);
    string S, T;
    getline(f1, S, '\\0');
    getline(f2, T, '\\0');
    
    string algo = argv[3];
    
    auto start = high_resolution_clock::now();
    int result = -1;
    
    if (algo == "recursive") {
        result = editDistanceRecursive(S, T, 0, 0);
    } else if (algo == "memo") {
        result = editDistanceMemoWrapper(S, T);
    } else if (algo == "dp") {
        result = editDistanceDP(S, T);
    } else if (algo == "dpopt") {
        result = editDistanceDPOptimized(S, T);
    }
    
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start).count();
    
    cout << result << " " << duration << endl;
    
    return 0;
}
"""
    with open('test_program.cpp', 'w') as f:
        f.write(codigo)

# Ejecutar experimentos
def ejecutar_experimentos():
    """Ejecuta las pruebas y guarda los resultados"""
    print("\nEjecutando experimentos...\n")
    
    archivos = ['text1.txt', 'text2.txt', 'text3.txt', 'text4.txt']
    algoritmos = ['memo', 'dp', 'dpopt']  # No usar recursive para textos grandes
    
    resultados = []
    
    for i, file1 in enumerate(archivos):
        for j, file2 in enumerate(archivos):
            if i != j:  # No comparar un archivo consigo mismo
                print(f"Probando {file1} -> {file2}")
                
                for algo in algoritmos:
                    # Solo usar recursive con text1
                    if algo == 'recursive' and (i > 0 or j > 0):
                        continue
                    
                    try:
                        cmd = f"./test_program {file1} {file2} {algo}"
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                        
                        if result.returncode == 0:
                            parts = result.stdout.strip().split()
                            distance = int(parts[0])
                            time_us = int(parts[1])
                            time_ms = time_us / 1000
                            
                            resultados.append({
                                'from': file1,
                                'to': file2,
                                'algo': algo,
                                'distance': distance,
                                'time_ms': time_ms
                            })
                            print(f"  {algo}: d={distance}, t={time_ms:.2f}ms")
                    except:
                        print(f"  {algo}: timeout o error")
    
    return resultados

# Crear gráficos simples
def crear_graficos(resultados):
    """Crea gráficos simples para el informe"""
    print("\nCreando gráficos...")
    
    # Preparar datos por algoritmo
    datos_algo = {}
    for r in resultados:
        algo = r['algo']
        if algo not in datos_algo:
            datos_algo[algo] = []
        datos_algo[algo].append(r['time_ms'])
    
    # Figura 1: Comparación de tiempos promedio
    plt.figure(figsize=(8, 6))
    
    algoritmos = list(datos_algo.keys())
    promedios = [sum(datos_algo[a])/len(datos_algo[a]) for a in algoritmos]
    
    bars = plt.bar(algoritmos, promedios, color=['#4CAF50', '#2196F3', '#FF9800'])
    plt.ylabel('Tiempo promedio (ms)')
    plt.title('Comparación de Algoritmos')
    
    # Agregar valores encima de las barras
    for bar, prom in zip(bars, promedios):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{prom:.1f}', ha='center')
    
    plt.tight_layout()
    plt.savefig('figura1_comparacion.png', dpi=150)
    plt.close()
    
    # Figura 2: Tiempos por pares de textos (solo DP y DP Optimizada)
    plt.figure(figsize=(10, 6))
    
    # Filtrar solo dp y dpopt
    resultados_dp = [r for r in resultados if r['algo'] in ['dp', 'dpopt']]
    
    # Agrupar por pares
    pares = []
    tiempos_dp = []
    tiempos_dpopt = []
    
    for r in resultados_dp:
        par = f"{r['from'][:-4]}->{r['to'][:-4]}"
        if r['algo'] == 'dp' and par not in pares:
            pares.append(par)
            tiempos_dp.append(r['time_ms'])
        elif r['algo'] == 'dpopt':
            idx = pares.index(par) if par in pares else -1
            if idx >= 0:
                if len(tiempos_dpopt) <= idx:
                    tiempos_dpopt.extend([0] * (idx + 1 - len(tiempos_dpopt)))
                tiempos_dpopt[idx] = r['time_ms']
    
    x = range(len(pares))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], tiempos_dp, width, label='DP', color='#2196F3')
    plt.bar([i + width/2 for i in x], tiempos_dpopt, width, label='DP Optimizada', color='#FF9800')
    
    plt.xlabel('Pares de textos')
    plt.ylabel('Tiempo (ms)')
    plt.title('Comparación DP vs DP Optimizada')
    plt.xticks(x, pares, rotation=45, ha='right')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('figura2_detalle.png', dpi=150)
    plt.close()
    
    print("Gráficos guardados: figura1_comparacion.png y figura2_detalle.png")

# Main
def main():
    print("=== EXPERIMENTO EDIT DISTANCE ===\n")
    
    # Cambiar al directorio correcto
    import os
    os.chdir('/Users/nico/Desktop/Universidad/Analisis/analisis-algoritmos-tarea2/experimental')
    
    # 1. Crear textos
    crear_textos()
    
    # 2. Crear programa de prueba
    crear_programa_prueba()
    
    # 3. Compilar
    compilar()
    
    # 4. Ejecutar experimentos
    resultados = ejecutar_experimentos()
    
    # 5. Crear gráficos
    if resultados:
        crear_graficos(resultados)
        print("\n¡Experimento completado!")
    else:
        print("\nNo se obtuvieron resultados")

if __name__ == "__main__":
    main()