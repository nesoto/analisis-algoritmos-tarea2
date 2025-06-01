# Makefile para Tarea 2: Delete Insert Edit Distance
# Análisis de Algoritmos - Universidad de Concepción

# Compilador y flags
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

# Archivos fuente
SOURCES = main.cpp recursive.cpp memo.cpp pdinamic.cpp pdopti.cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = editdistance

# Regla principal
all: $(TARGET)

# Crear el ejecutable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

# Compilar archivos objeto
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Ejecutar el programa
run: $(TARGET)
	./$(TARGET)

# Limpiar archivos generados
clean:
	rm -f $(OBJECTS) $(TARGET)

# Compilar en modo debug
debug: CXXFLAGS += -g -DDEBUG
debug: $(TARGET)

# Ejecutar con valgrind para detectar memory leaks
valgrind: $(TARGET)
	valgrind --leak-check=full ./$(TARGET)

# Reglas que no crean archivos
.PHONY: all run clean debug valgrind

# Información del proyecto
info:
	@echo "Tarea 2: Delete Insert Edit Distance"
	@echo "Archivos fuente: $(SOURCES)"
	@echo "Ejecutable: $(TARGET)"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make         - Compilar el proyecto"
	@echo "  make run     - Compilar y ejecutar"
	@echo "  make clean   - Limpiar archivos generados"
	@echo "  make debug   - Compilar en modo debug"
	@echo "  make valgrind- Ejecutar con valgrind"
	@echo "  make info    - Mostrar esta información"