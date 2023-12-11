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
        line= re.sub(r'[^a-zA-Z ]', '', line)
        if keyword == line:
            # Busca la próxima línea que no esté en blanco
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    # Imprime la información después de la keyword
                    x = (lines[j].strip())
                    break 
    return numero_digitos, re.sub(r'[^a-zA-Z ]', '', x)


def save_text_to_txt(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def main(inpu):
    path = 'D:\Clinica sanens sem2\\'
    pdf_path = path+(inpu)+'.pdf'
    page_number = 1
    # Ajusta la resolución y el contraste según tus necesidades
    resolution = 150
    contrast_factor = 1.5

    image = pdf_to_bw_image(pdf_path, page_number, resolution, contrast_factor)

    text = ocr_from_image(image)

    numero_8_digitos, palabras_despues_paciente = extract_information(text)

    output_path = 'output.txt'
    save_text_to_txt(text, output_path)

    nombre = str (inpu[0:5] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
    print (nombre)

    nuevo_path = path+nombre+".pdf"
    with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
         nombre_file.write(nuevo_path)

    respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
    
    respuesta = respuesta.lower()
    if respuesta == 'y' or respuesta == 'Y':
        # Cambia el nombre del archivo

        with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
            nuevo_nombre = nombre_file.read().strip()
            os.rename(pdf_path, nuevo_nombre)
        print(f"El nombre del archivo ha sido cambiado a: {nuevo_path}")

    elif(respuesta == 'i'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,8,'PACIENTEI')
        nombre = str (inpu[0:5] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        print (nombre)

        nuevo_path = path+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)
        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/N): ").lower()
    

        if respuesta == 'y' or respuesta == 'Y':
        # Cambia el nombre del archivo
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: {nuevo_path}")
        
    elif(respuesta == '9'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,9)
        nombre = str (inpu[0:5] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        print (nombre)

        nuevo_path = path+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)

        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
        
        if respuesta == 'y' or respuesta == 'Y':
        # Cambia el nombre del archivo
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: {nuevo_path}")
    elif(respuesta == '2'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,8, 'DATOS PERSONALES')
        nombre = str (inpu[0:5] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        print (nombre)

        nuevo_path = path+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)
        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
        
        if respuesta == 'y' or respuesta == 'Y':
        # Cambia el nombre del archivo
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: {nuevo_path}")
if __name__ == "__main__":
    archivo_nombres_sin_extension = "nombres_sin_extension.txt"

    # Leer el archivo y imprimir cada línea
    with open(archivo_nombres_sin_extension, "r") as archivo_txt:
        lineas = archivo_txt.readlines()
        for linea in lineas:
            # Eliminar caracteres de nueva línea y espacios adicionales
            nombre_limpiado = linea.strip()
            main(nombre_limpiado)

