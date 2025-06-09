#!/usr/bin/env python3
"""
Script automático para descargar y preparar textos de Project Gutenberg
"""

import urllib.request
import re
import os

def download_and_prepare_texts():
    """
    Descarga Pride and Prejudice de Project Gutenberg y prepara los 4 extractos
    """
    print("=== DESCARGA AUTOMÁTICA DE TEXTOS DE PROJECT GUTENBERG ===\n")
    
    # URL de Pride and Prejudice
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    
    print(f"Descargando Pride and Prejudice desde:\n{url}\n")
    
    try:
        # Descargar el texto
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
        print("✓ Texto descargado exitosamente\n")
    except Exception as e:
        print(f"✗ Error al descargar: {e}")
        print("\nAlternativa: descarga manualmente desde el navegador")
        return False
    
    # Encontrar el inicio del libro (después de los encabezados de Gutenberg)
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("✗ No se encontraron los marcadores del libro")
        return False
    
    # Extraer solo el contenido del libro
    book_text = text[start_idx:end_idx]
    
    # Buscar el Capítulo 1
    chapter1_start = book_text.find("Chapter 1")
    if chapter1_start == -1:
        chapter1_start = book_text.find("CHAPTER 1")
    if chapter1_start == -1:
        chapter1_start = book_text.find("Chapter I")
    
    if chapter1_start == -1:
        print("✗ No se encontró el Capítulo 1")
        return False
    
    # Buscar el Capítulo 2 para saber dónde termina el 1
    chapter2_start = book_text.find("Chapter 2", chapter1_start + 10)
    if chapter2_start == -1:
        chapter2_start = book_text.find("CHAPTER 2", chapter1_start + 10)
    if chapter2_start == -1:
        chapter2_start = book_text.find("Chapter II", chapter1_start + 10)
    
    # Extraer el capítulo 1 completo
    if chapter2_start != -1:
        chapter1_full = book_text[chapter1_start:chapter2_start]
    else:
        # Si no encontramos el capítulo 2, tomamos aproximadamente 5000 caracteres
        chapter1_full = book_text[chapter1_start:chapter1_start + 10000]
    
    # Limpiar el texto
    chapter1_full = re.sub(r'Chapter [1I]\s*', '', chapter1_full, count=1)
    chapter1_full = re.sub(r'\s+', ' ', chapter1_full).strip()
    
    # Dividir en palabras
    words = chapter1_full.split()
    
    # Crear los 4 extractos
    texts = {
        'text1.txt': {
            'content': ' '.join(words[:20]),  # Primera oración aprox
            'description': 'Pride and Prejudice - Primera oración (~20 palabras)',
            'words': 20
        },
        'text2.txt': {
            'content': ' '.join(words[:75]),  # Primer párrafo
            'description': 'Pride and Prejudice - Primer párrafo (~75 palabras)',
            'words': 75
        },
        'text3.txt': {
            'content': ' '.join(words[:500]),  # Primera página
            'description': 'Pride and Prejudice - Primera página (~500 palabras)',
            'words': 500
        },
        'text4.txt': {
            'content': ' '.join(words[:1500]),  # Más del capítulo
            'description': 'Pride and Prejudice - Capítulo 1 (~1500 palabras)',
            'words': 1500
        }
    }
    
    # Guardar los archivos
    print("Creando archivos de texto:\n")
    
    for filename, info in texts.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(info['content'])
        
        actual_words = len(info['content'].split())
        byte_count = len(info['content'].encode('utf-8'))
        
        print(f"✓ {filename}:")
        print(f"  - {info['description']}")
        print(f"  - {actual_words} palabras, {byte_count} bytes")
        print(f"  - Primeras palabras: \"{' '.join(info['content'].split()[:10])}...\"\n")
    
    print("✓ Archivos creados exitosamente!")
    print("\nPuedes ejecutar ahora: python3 experiment_simple.py")
    
    return True

def main():
    os.chdir('/Users/nico/Desktop/Universidad/Analisis/analisis-algoritmos-tarea2/experimental')
    download_and_prepare_texts()

if __name__ == "__main__":
    main()
