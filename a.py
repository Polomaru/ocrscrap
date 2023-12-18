import fitz
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import re
import os

def pdf_to_bw_image(pdf_path, page_number, resolution=600, contrast_factor=2.0):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number - 1)

    # Ajusta la resolución deseada
    zoom_factor = resolution / 72.0  # 72 DPI es la resolución estándar
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))

    # Convierte el pixmap a una imagen
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Ajusta el contraste
    enhancer = ImageEnhance.Contrast(image)
    image_contrasted = enhancer.enhance(contrast_factor)

    # Convierte la imagen a blanco y negro
    image_bw = ImageOps.grayscale(image_contrasted)

    return image_bw

def ocr_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def extract_information(text,num_digits=8, keyword='PACIENTE'):
    match_numero = re.search(rf'\b\d{{{num_digits}}}\b', text)
    numero_digitos = match_numero.group() if match_numero else ''

    x = ''
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line = re.sub(r'[^a-zA-Z ]', '', line)
        line = line.replace(" ", "").replace("  ", "") 
        if keyword == line:
            # Busca la próxima línea que no esté en blanco
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    # Imprime la información después de la keyword
                    x = (lines[j].strip())
                    break 
    x = re.sub(r'[^a-zA-Z ]', '', x)

    t = x.split()
    x=''
    for i in t:
        if len(i)>2 or i=="DE" or i=="LA" or i=="DA" or i=="FE":
            if i=="NUNEZ":
                x=x+"NUÑEZ"+" "
            elif i=="PENA":
                x=x+"PEÑA"+" "
            elif i=="ACUNA":
                x=x+"ACUÑA"+" "
            elif i=="BRENA":
                x=x+"BREÑA"+" "
            elif i=="ZUNIGA":
                x=x+"ZUÑIGA"+" "
            elif i=="MUNOZ":
                x=x+"MUÑOZ"+" "
            elif i=="CASTANEDA":
                x=x+"CASTAÑEDA"+" "
            elif i=="ORMENO":
                x=x+"ORMEÑO"+" "
            elif i=="RUBINOS":
                x=x+"RUBIÑOS"+" "
            elif i=="SALDANA":
                x=x+"SALDAÑA"+" "
            elif i=="IBANEZ":
                x=x+"IBAÑEZ"+" "
            elif i=="REANO":
                x=x+"REAÑO"+" "
            elif i=="QUINONES":
                x=x+"QUIÑONES"+" "
            elif i=="QUINONEZ":
                x=x+"QUIÑONEZ"+" "
            elif i=="SUANA":
                x=x+"SUAÑA"+" "
            else:
                x=x+i+" "
    
    return numero_digitos, x[0:len(x)-1]


def save_text_to_txt(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
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

imagen_salida = "ps.png"

def main(inpu,t):
    path = 'D:\CLINICA SANENS\Clinica sanens sem3\\'
    pdf_path = path+(inpu)+'.pdf'
    page_number = 1
    # Ajusta la resolución y el contraste según tus necesidades
    resolution = 150
    contrast_factor = 1.5

    convertir_pdf_a_imagen(pdf_path, imagen_salida)
    
    image = pdf_to_bw_image(pdf_path, page_number, resolution, contrast_factor)

    text = ocr_from_image(image)

    numero_8_digitos, palabras_despues_paciente = extract_information(text)

    output_path = 'output.txt'
    save_text_to_txt(text, output_path)

    nombre = str (inpu[0:t] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
    nombre = nombre.replace("  ", " ").replace("   ", " ")
    print()
    print (nombre)

    nuevo_path = path+nombre+".pdf"
    with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
         nombre_file.write(nuevo_path)

    print()
    respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
    
    respuesta = respuesta.lower()
    if respuesta == 'y' or respuesta == 'Y' or respuesta == "":
        # Cambia el nombre del archivo

        nuevo_nombre=""
        with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
            nuevo_nombre = nombre_file.read().strip()
            os.rename(pdf_path, nuevo_nombre)
        print()
        print("El nombre del archivo ha sido cambiado a:")
        print(nuevo_nombre)
    elif(respuesta == 'i'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,8,'PACIENTEI')
        nombre = str (inpu[0:t] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        nombre = nombre.replace("  ", " ")
        print (nombre)

        nuevo_path = path+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)
        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/N): ").lower()
    

        if respuesta == 'y' or respuesta == 'Y' or respuesta == "":
        # Cambia el nombre del archivo
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print()
            print("El nombre del archivo ha sido cambiado a:")
            print(nuevo_nombre)
    elif(respuesta == '9'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,9)
        nombre = str (inpu[0:t] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        nombre = nombre.replace("  ", " ")
        print (nombre)

        nuevo_path = path+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)

        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
        
        if respuesta == 'y' or respuesta == 'Y' or respuesta == "":
        # Cambia el nombre del archivo
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: ")
            print(nuevo_path)
            print()
        else:
            print("repit")
            print()
            main(inpu)
    elif(respuesta == 'r'):
        print("repit")
        print()
        main(inpu)
    else:
        print("repit")
        print()
        main(inpu)
if __name__ == "__main__":
    archivo_nombres_sin_extension = "nombres_sin_extension.txt"

    t = int(input("N: "))
    while True:
        # Leer la primera fila
        with open(archivo_nombres_sin_extension, 'r') as archivo:
            primer_fila = archivo.readline().strip()

        # Verificar si se llegó al final del archivo
        if not primer_fila:
            print("Fin del archivo. No hay más filas para procesar.")
            break

        main(primer_fila,t)

        # Eliminar la primera fila
        with open(archivo_nombres_sin_extension, 'r') as archivo:
            lineas = archivo.readlines()

        with open(archivo_nombres_sin_extension, 'w') as archivo:
            archivo.writelines(lineas[1:])
