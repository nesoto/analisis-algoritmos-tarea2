#!/usr/bin/env python3
"""
Generador de gráficos para los resultados experimentales
"""

import json
import matplotlib.pyplot as plt
import numpy as np

def load_results():
    """Carga los resultados del experimento"""
    with open('results_direct.json', 'r') as f:
        return json.load(f)

def create_plots(results):
    """Crea los gráficos para el informe"""
    
    # Preparar datos
    data_by_algo = {}
    for r in results:
        algo = r['algorithm']
        if algo not in data_by_algo:
            data_by_algo[algo] = {
                'pairs': [],
                'times': [],
                'distances': []
            }
        
        pair = f"{r['from'][:-4]}->{r['to'][:-4]}"  # Quitar .txt
        data_by_algo[algo]['pairs'].append(pair)
        data_by_algo[algo]['times'].append(r['time_ms'])
        data_by_algo[algo]['distances'].append(r['distance'])
    
    # Crear figura con subplots
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Gráfico de barras: Tiempo por algoritmo y par de textos
    ax1 = plt.subplot(2, 2, 1)
    
    # Obtener todos los pares únicos
    all_pairs = []
    for r in results:
        pair = f"{r['from'][:-4]}->{r['to'][:-4]}"
        if pair not in all_pairs:
            all_pairs.append(pair)
    
    # Colores para cada algoritmo
    colors = {'recursive': '#ff6b6b', 'memo': '#4ecdc4', 'dp': '#45b7d1', 'dpopt': '#f9ca24'}
    
    # Ancho de las barras
    n_algos = len(data_by_algo)
    width = 0.8 / n_algos
    x = np.arange(len(all_pairs))
    
    # Crear barras para cada algoritmo
    for i, (algo, data) in enumerate(data_by_algo.items()):
        # Alinear tiempos con pares
        times_aligned = []
        for pair in all_pairs:
            if pair in data['pairs']:
                idx = data['pairs'].index(pair)
                times_aligned.append(data['times'][idx])
            else:
                times_aligned.append(0)
        
        offset = (i - n_algos/2) * width + width/2
        ax1.bar(x + offset, times_aligned, width, label=algo, color=colors.get(algo, 'gray'))
    
    ax1.set_xlabel('Pares de textos')
    ax1.set_ylabel('Tiempo (ms)')
    ax1.set_title('Tiempo de Ejecución por Algoritmo')
    ax1.set_xticks(x)
    ax1.set_xticklabels(all_pairs, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, axis='y', alpha=0.3)
    
    # 2. Gráfico de líneas: Escalabilidad
    ax2 = plt.subplot(2, 2, 2)
    
    # Mapear tamaños aproximados
    text_sizes = {
        'text1': 100,    # ~15 palabras
        'text2': 500,    # ~75 palabras
        'text3': 5000,   # ~1000 palabras
        'text4': 25000   # ~5000 palabras
    }
    
    for algo in ['memo', 'dp', 'dpopt']:  # Excluir recursive
        if algo in data_by_algo:
            sizes = []
            times = []
            
            for i, pair in enumerate(data_by_algo[algo]['pairs']):
                parts = pair.split('->')
                size = text_sizes[parts[0]] + text_sizes[parts[1]]
                sizes.append(size)
                times.append(data_by_algo[algo]['times'][i])
            
            # Ordenar por tamaño
            sorted_data = sorted(zip(sizes, times))
            sizes_sorted = [x[0] for x in sorted_data]
            times_sorted = [x[1] for x in sorted_data]
            
            ax2.plot(sizes_sorted, times_sorted, 'o-', label=algo, 
                    color=colors.get(algo, 'gray'), linewidth=2, markersize=8)
    
    ax2.set_xlabel('Tamaño total aproximado (caracteres)')
    ax2.set_ylabel('Tiempo (ms)')
    ax2.set_title('Escalabilidad de los Algoritmos')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Comparación de tiempos promedio
    ax3 = plt.subplot(2, 2, 3)
    
    algos = []
    avg_times = []
    std_times = []
    
    for algo in ['memo', 'dp', 'dpopt']:  # Orden específico
        if algo in data_by_algo:
            algos.append(algo)
            times = data_by_algo[algo]['times']
            avg_times.append(np.mean(times))
            std_times.append(np.std(times))
    
    y_pos = np.arange(len(algos))
    bars = ax3.barh(y_pos, avg_times, xerr=std_times, 
                    color=[colors.get(a, 'gray') for a in algos], alpha=0.8)
    
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(algos)
    ax3.set_xlabel('Tiempo promedio (ms)')
    ax3.set_title('Comparación de Tiempos Promedio')
    ax3.grid(True, axis='x', alpha=0.3)
    
    # Agregar valores en las barras
    for i, (bar, avg) in enumerate(zip(bars, avg_times)):
        ax3.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{avg:.2f}', va='center')
    
    # 4. Matriz de distancias como heatmap
    ax4 = plt.subplot(2, 2, 4)
    
    # Crear matriz de distancias
    texts = ['text1', 'text2', 'text3', 'text4']
    matrix = np.zeros((4, 4))
    
    # Usar resultados de DP como referencia
    dp_results = [r for r in results if r['algorithm'] == 'dp']
    
    for r in dp_results:
        i = texts.index(r['from'][:-4])
        j = texts.index(r['to'][:-4])
        matrix[i][j] = r['distance']
    
    # Crear heatmap
    im = ax4.imshow(matrix, cmap='YlOrRd')
    
    # Configurar ticks
    ax4.set_xticks(np.arange(4))
    ax4.set_yticks(np.arange(4))
    ax4.set_xticklabels(texts)
    ax4.set_yticklabels(texts)
    
    # Rotar labels
    plt.setp(ax4.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Agregar valores en las celdas
    for i in range(4):
        for j in range(4):
            text = ax4.text(j, i, int(matrix[i, j]), 
                           ha="center", va="center", color="black")
    
    ax4.set_title("Matriz de Distancias de Edición")
    fig.colorbar(im, ax=ax4)
    
    plt.tight_layout()
    plt.savefig('resultados_experimentales.png', dpi=300, bbox_inches='tight')
    print("Gráficos guardados en resultados_experimentales.png")
    
    # Crear segundo gráfico con zoom en algoritmos eficientes
    plt.figure(figsize=(12, 5))
    
    # Filtrar solo algoritmos eficientes
    efficient_results = [r for r in results if r['algorithm'] in ['memo', 'dp', 'dpopt']]
    
    # Gráfico 1: Comparación detallada
    plt.subplot(1, 2, 1)
    
    # Reorganizar datos por par
    pairs_data = {}
    for r in efficient_results:
        pair = f"{r['from'][:-4]}->{r['to'][:-4]}"
        if pair not in pairs_data:
            pairs_data[pair] = {}
        pairs_data[pair][r['algorithm']] = r['time_ms']
    
    # Crear gráfico de barras agrupadas
    pairs = list(pairs_data.keys())
    x = np.arange(len(pairs))
    width = 0.25
    
    for i, algo in enumerate(['memo', 'dp', 'dpopt']):
        times = [pairs_data[p].get(algo, 0) for p in pairs]
        offset = (i - 1) * width
        plt.bar(x + offset, times, width, label=algo, color=colors.get(algo, 'gray'))
    
    plt.xlabel('Pares de textos')
    plt.ylabel('Tiempo (ms)')
    plt.title('Comparación Detallada de Algoritmos Eficientes')
    plt.xticks(x, pairs, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y', alpha=0.3)
    
    # Gráfico 2: Speedup relativo
    plt.subplot(1, 2, 2)
    
    # Calcular speedup de dpopt respecto a dp
    speedups = []
    labels = []
    
    for pair in pairs_data:
        if 'dp' in pairs_data[pair] and 'dpopt' in pairs_data[pair]:
            dp_time = pairs_data[pair]['dp']
            dpopt_time = pairs_data[pair]['dpopt']
            if dpopt_time > 0:
                speedup = dp_time / dpopt_time
                speedups.append(speedup)
                labels.append(pair)
    
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, speedups, color='#f9ca24', alpha=0.8)
    plt.yticks(y_pos, labels)
    plt.xlabel('Speedup (DP / DP Optimizada)')
    plt.title('Mejora de DP Optimizada vs DP Estándar')
    plt.axvline(x=1, color='red', linestyle='--', alpha=0.5)
    plt.grid(True, axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('resultados_detallados.png', dpi=300, bbox_inches='tight')
    print("Gráficos detallados guardados en resultados_detallados.png")
    
    plt.show()

def main():
    print("Cargando resultados...")
    results = load_results()
    
    print(f"Encontrados {len(results)} resultados experimentales")
    
    print("Generando gráficos...")
    create_plots(results)
    
    print("\n¡Gráficos generados exitosamente!")

if __name__ == "__main__":
    main()
