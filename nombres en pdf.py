import os

# Ruta de la carpeta
carpeta = "D:\Clinica sanens sem2"

# Obtener la lista de archivos en la carpeta
archivos = os.listdir(carpeta)

# Crear un archivo de texto para escribir los nombres sin extensión
with open("nombres_sin_extension.txt", "w") as archivo_txt:
    # Escribir cada nombre de archivo sin extensión en una nueva línea
    for nombre_archivo in archivos:
        nombre_sin_extension, _ = os.path.splitext(nombre_archivo)
        archivo_txt.write(nombre_sin_extension + "\n")

print("Nombres de archivos (sin extensión) extraídos y guardados en nombres_sin_extension.txt")
