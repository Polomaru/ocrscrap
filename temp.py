def leer_imprimir_eliminar_primera_fila(nombre_archivo):
    while True:
        # Leer la primera fila
        with open(nombre_archivo, 'r') as archivo:
            primer_fila = archivo.readline().strip()

        # Verificar si se llegó al final del archivo
        if not primer_fila:
            print("Fin del archivo. No hay más filas para procesar.")
            break

        print(f"Primera fila: {primer_fila}")

        # Esperar a que el usuario presione Enter
        input("Presiona Enter para continuar...")

        # Eliminar la primera fila
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        with open(nombre_archivo, 'w') as archivo:
            archivo.writelines(lineas[1:])

# Reemplaza 'nombre_del_archivo.txt' con el nombre real de tu archivo
nombre_archivo = 'nombres_sin_extension.txt'

# Llama a la función para realizar las operaciones en un bucle
leer_imprimir_eliminar_primera_fila(nombre_archivo)
