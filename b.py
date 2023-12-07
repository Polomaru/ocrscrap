# Ruta del archivo que contiene los nombres sin extensión
archivo_nombres_sin_extension = "nombres_sin_extension.txt"

# Leer el archivo y imprimir cada línea
with open(archivo_nombres_sin_extension, "r") as archivo_txt:
    lineas = archivo_txt.readlines()
    for linea in lineas:
        # Eliminar caracteres de nueva línea y espacios adicionales
        nombre_limpiado = linea.strip()
        print(nombre_limpiado)
        lineas.remove(linea)