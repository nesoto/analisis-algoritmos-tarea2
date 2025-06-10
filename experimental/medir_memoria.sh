#!/bin/bash
# Script simple para medir memoria de los algoritmos

echo "=== MEDICIÓN DE MEMORIA ==="
echo ""

# Compilar si no existe
if [ ! -f test_program ]; then
    echo "Compilando programa..."
    g++ -std=c++17 -O2 -o test_program test_program.cpp ../recursive.cpp ../memo.cpp ../pdinamic.cpp ../dpopti.cpp
fi

echo "Midiendo uso de memoria para text3.txt -> text4.txt:"
echo ""

# Medir memoria para cada algoritmo
for algo in memo dp dpopt; do
    echo -n "$algo: "
    /usr/bin/time -f "%M KB" ./test_program text3.txt text4.txt $algo 2>&1 | grep "KB"
done

echo ""
echo "Nota: El algoritmo recursivo no se prueba con textos grandes porque tomaría mucho tiempo"