#!/usr/bin/env python3
"""
Script para preparar textos de Project Gutenberg para el experimento
"""

import os

def create_gutenberg_texts():
    """
    Crea los 4 archivos de texto basados en Pride and Prejudice de Project Gutenberg
    
    URL del libro: https://www.gutenberg.org/files/1342/1342-0.txt
    """
    
    # Textos extraídos manualmente de Pride and Prejudice
    # Puedes cambiarlos por extractos de cualquier libro de Gutenberg
    
    texts = {
        'text1.txt': {
            'content': "It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife",
            'description': 'Pride and Prejudice - Primera oración (22 palabras)',
            'source': 'Capítulo 1, primera oración'
        },
        'text2.txt': {
            'content': """It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood this truth is so well fixed in the minds of the surrounding families that he is considered as the rightful property of some one or other of their daughters""",
            'description': 'Pride and Prejudice - Primer párrafo (69 palabras)',
            'source': 'Capítulo 1, párrafo completo'
        },
        'text3.txt': {
            'content': """It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood this truth is so well fixed in the minds of the surrounding families that he is considered as the rightful property of some one or other of their daughters. My dear Mr Bennet said his lady to him one day have you heard that Netherfield Park is let at last. Mr Bennet replied that he had not. But it is returned she for Mrs Long has just been here and she told me all about it. Mr Bennet made no answer. Do not you want to know who has taken it cried his wife impatiently. You want to tell me and I have no objection to hearing it. This was invitation enough. Why my dear you must know Mrs Long says that Netherfield is taken by a young man of large fortune from the north of England that he came down on Monday in a chaise and four to see the place and was so much delighted with it that he agreed with Mr Morris immediately that he is to take possession before Michaelmas and some of his servants are to be in the house by the end of next week. What is his name. Bingley. Is he married or single. Oh single my dear to be sure A single man of large fortune four or five thousand a year What a fine thing for our girls. How so how can it affect them. My dear Mr Bennet replied his wife how can you be so tiresome You must know that I am thinking of his marrying one of them. Is that his design in settling here. Design nonsense how can you talk so But it is very likely that he may fall in love with one of them and therefore you must visit him as soon as he comes. I see no occasion for that You and the girls may go or you may send them by themselves which perhaps will be still better for as you are as handsome as any of them Mr Bingley might like you the best of the party""",
            'description': 'Pride and Prejudice - Primera página (~400 palabras)',
            'source': 'Capítulo 1, primera página'
        },
        'text4.txt': {
            'content': """[AQUÍ DEBERÍAS PEGAR EL CAPÍTULO 1 COMPLETO DE PRIDE AND PREJUDICE]
            
            Para obtenerlo:
            1. Ve a https://www.gutenberg.org/files/1342/1342-0.txt
            2. Busca "Chapter 1" 
            3. Copia todo el texto hasta "Chapter 2"
            4. Pégalo aquí reemplazando este texto
            
            El capítulo 1 completo tiene aproximadamente 1200 palabras.""",
            'description': 'Pride and Prejudice - Capítulo 1 completo (~1200 palabras)',
            'source': 'Capítulo 1 completo'
        }
    }
    
    print("Creando archivos de texto de Project Gutenberg...")
    print("Fuente: Pride and Prejudice de Jane Austen")
    print("URL: https://www.gutenberg.org/files/1342/1342-0.txt\n")
    
    for filename, info in texts.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(info['content'])
        
        word_count = len(info['content'].split())
        byte_count = len(info['content'].encode('utf-8'))
        
        print(f"✓ {filename}:")
        print(f"  - {info['description']}")
        print(f"  - {word_count} palabras, {byte_count} bytes")
        print(f"  - Fuente: {info['source']}\n")
    
    return texts

def main():
    print("=== PREPARACIÓN DE TEXTOS DE PROJECT GUTENBERG ===\n")
    
    # Crear directorio si no existe
    if not os.path.exists('texts'):
        os.makedirs('texts')
    
    os.chdir('texts')
    
    # Crear los archivos
    create_gutenberg_texts()
    
    print("\nINSTRUCCIONES:")
    print("1. Para text4.txt, necesitas copiar el Capítulo 1 completo de Pride and Prejudice")
    print("2. Ve a: https://www.gutenberg.org/files/1342/1342-0.txt")
    print("3. Busca 'Chapter 1' y copia todo hasta 'Chapter 2'")
    print("4. Reemplaza el contenido placeholder en text4.txt")
    print("\nAlternativamente, puedes usar cualquier otro libro de Project Gutenberg")
    print("siguiendo la misma estructura de tamaños.")

if __name__ == "__main__":
    main()
