import fitz  # PyMuPDF
from PIL import Image

def convertir_pdf_a_imagen(pdf_path, imagen_salida):
    # Abrir el archivo PDF
    pdf_documento = fitz.open(pdf_path)

    # Obtener la primera página
    pagina = pdf_documento[0]

    # Obtener las dimensiones de la página
    ancho, alto = pagina.mediabox_size

    # Definir las coordenadas de la parte superior de la página (ajusta según tus necesidades)
    x0, y0, x1, y1 = 0, 0, ancho, alto // 2

    # Extraer la región de la parte superior de la página como una imagen
    region = fitz.Rect(x0, y0, x1, y1)
    imagen = pagina.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72), clip=region)

    # Guardar la imagen
    imagen.save(imagen_salida)

    # Cerrar el documento PDF
    pdf_documento.close()

if __name__ == "__main__":
    # Ruta del archivo PDF de entrada
    pdf_path = "E:\\CLINICA SANENS\\Clinica sanens sem1\\12011.pdf"

    # Ruta de la imagen de salida
    imagen_salida = "parte_superior_pagina.png"

    # Convertir PDF a imagen
    convertir_pdf_a_imagen(pdf_path, imagen_salida)

    print(f"La imagen se ha guardado en: {imagen_salida}")
