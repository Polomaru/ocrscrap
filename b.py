import os
import PyPDF2

def contar_paginas_pdf(carpeta):
    total_paginas = 0

    for directorio_actual, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            if archivo.endswith(".pdf"):
                ruta_completa = os.path.join(directorio_actual, archivo)
                with open(ruta_completa, "rb") as file:
                    pdf_reader = PyPDF2.PdfFileReader(file)
                    total_paginas += pdf_reader.numPages

    return total_paginas

# Ruta de la carpeta en el USB (cambia la letra de unidad según sea necesario)
carpeta_pdf_usb = "E:/"

# Llamada a la función para contar páginas
total_paginas = contar_paginas_pdf(carpeta_pdf_usb)

print(f"El total de páginas en los archivos PDF en el USB ({carpeta_pdf_usb}) es: {total_paginas}")
