import sqlite3
import fitz  # lector de pdfs
import os
import re

DB_PATH = "../data/raw/legal_database.sqlite"  # Ruta de la base de datos
PDF_PATH = "../data/docs/ReglamentoTransito.pdf"  # Ruta específica del archivo a procesar

def extract_text_from_pdf(pdf_path):
    """Extrae el texto completo de un PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def split_text_into_articles(text):
    """
    Divide el texto en artículos utilizando como delimitador la palabra "Artículo" seguida de un número.
    Retorna una lista de tuplas (numero_articulo, contenido_del_artículo).
    """
    parts = re.split(r'(Artículo\s+\d+)', text)
    articles = []
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            article_header = parts[i].strip()  # Ejemplo: "Artículo 1"
            article_content = parts[i+1].strip() if (i+1) < len(parts) else ""
            articles.append((article_header, article_content))
    else:
        articles.append(("", text))
    return articles

def split_article_into_subsections(text):
    """
    Divide el contenido de un artículo en contenido principal y subapartados.
    Se asume que los subapartados comienzan con números romanos seguidos de un punto y un espacio (ej: "I. ").
    
    Retorna:
    - main_text: el contenido principal (antes del primer subapartado)
    - subsections: lista de tuplas (numero_sub, contenido_sub)
    """
    pattern = r'(\b[IVXLCDM]+\.\s)'
    parts = re.split(pattern, text)
    if len(parts) < 3:
        return text.strip(), []
    
    main_text = parts[0].strip()
    subsections = []
    for i in range(1, len(parts)-1, 2):
        marker = parts[i].strip()  # Ejemplo: "I."
        content = parts[i+1].strip()
        subsections.append((marker.rstrip('.'), content))
    return main_text, subsections

def save_article_and_subsections(fuente, numero_articulo, contenido_articulo, subsections):
    """
    Guarda el artículo en la tabla 'articulos' y sus subapartados en 'sub_articulos'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO articulos (fuente, numero, contenido) VALUES (?, ?, ?)",
        (fuente, numero_articulo, contenido_articulo)
    )
    article_id = cursor.lastrowid
    
    for sub_num, sub_content in subsections:
        cursor.execute(
            "INSERT INTO sub_articulos (articulo_id, numero, contenido) VALUES (?, ?, ?)",
            (article_id, sub_num, sub_content)
        )
    conn.commit()
    conn.close()

def process_reglamento_transito():
    """Procesa solo el archivo ReglamentoTransito.pdf y guarda sus artículos y subapartados en la base de datos."""
    if not os.path.exists(PDF_PATH):
        print(f"Error: No se encontró el archivo {PDF_PATH}")
        return

    print(f"Procesando: ReglamentoTransito.pdf")
    text = extract_text_from_pdf(PDF_PATH)
    articles = split_text_into_articles(text)
    for article_num, article_content in articles:
        if article_content:
            main_content, subsections = split_article_into_subsections(article_content)
            save_article_and_subsections("Reglamento de Tránsito", article_num, main_content, subsections)
            print(f"  Guardado: {article_num if article_num else 'Artículo único'} de ReglamentoTransito.pdf")
        else:
            print(f"  Advertencia: {article_num} sin contenido en ReglamentoTransito.pdf")

if __name__ == "__main__":
    process_reglamento_transito()
    print("Procesamiento del Reglamento de Tránsito completado.")
