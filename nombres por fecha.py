import os
import glob

def extract_pdf_names_by_modification_date(directory_path, output_file_path):
    # Obtener la lista de archivos PDF en el directorio
    pdf_files = glob.glob(os.path.join(directory_path, '*.pdf'))

    # Obtener los nombres y las fechas de modificación de los archivos PDF
    pdf_info = [(os.path.splitext(os.path.basename(pdf))[0], os.path.getmtime(pdf)) for pdf in pdf_files]

    # Ordenar la lista de archivos por fecha de modificación
    pdf_info.sort(key=lambda x: x[1])

    # Guardar los nombres en un archivo de texto
    with open(output_file_path, 'w') as output_file:
        for name, _ in pdf_info:
            output_file.write(name + '\n')

# Especifica el directorio donde se encuentran los archivos PDF
directorio_pdf = 'D:\Clinica sanens sem2'

# Especifica la ruta del archivo de texto de salida
archivo_txt_salida = 'nombres_por_fecha.txt'

# Llama a la función para extraer y guardar los nombres de los archivos PDF por fecha de modificación
extract_pdf_names_by_modification_date(directorio_pdf, archivo_txt_salida)
