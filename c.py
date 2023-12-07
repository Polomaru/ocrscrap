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

def extract_information(text, palabras_despues=3):
    # Busca el primer número de 8 dígitos
    match_numero = re.search(r'\b\d{8}\b', text)
    numero_8_digitos = match_numero.group() if match_numero else None

    # Busca las siguientes 4 palabras después de la palabra "PACIENTE" y las une en un string separado por espacio
    match_paciente = re.search('Nombres', text)
    palabras_despues_paciente = ''
    if match_paciente:
        start_index = match_paciente.end()  # Obtén la posición de la palabra "PACIENTE"
        palabras_despues_paciente = ' '.join(re.findall(r'\b\w+\b', text[start_index:start_index + palabras_despues * 10])[:palabras_despues])

    return numero_8_digitos, palabras_despues_paciente

def extract_information2(text, palabras_despues=3):
    # Busca el primer número de 8 dígitos
    match_numero = re.search(r'\b\d{8}\b', text)
    numero_8_digitos = match_numero.group() if match_numero else None

    # Busca las siguientes 4 palabras después de la palabra "PACIENTE" y las une en un string separado por espacio
    match_paciente = re.search(r'\bPACIENTEI\b', text)
    palabras_despues_paciente = ''
    if match_paciente:
        start_index = match_paciente.end()  # Obtén la posición de la palabra "PACIENTE"
        palabras_despues_paciente = ' '.join(re.findall(r'\b\w+\b', text[start_index:start_index + palabras_despues * 10])[:palabras_despues])

    return numero_8_digitos, palabras_despues_paciente

def save_text_to_txt(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def main():
    print()
    inpu = input("archivopdf:")
    pdf_path = 'E:\CLINICA SANENS\Clinica sanens sem1\\'+inpu+'.pdf'
    page_number = 1

    # Ajusta la resolución y el contraste según tus necesidades
    resolution = 150
    contrast_factor = 1.5
    x =int(input("ingrese numero de letras:" ))

    image = pdf_to_bw_image(pdf_path, page_number, resolution, contrast_factor)

    text = ocr_from_image(image)

    numero_8_digitos, palabras_despues_paciente = extract_information(text,x)

    output_path = 'output.txt'
    save_text_to_txt(text, output_path)

    nombre = str (inpu[0:4] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
    print (nombre)

    nuevo_path = "E:\CLINICA SANENS\Clinica sanens sem1\\"+nombre+".pdf"
    with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
         nombre_file.write(nuevo_path)

    respuesta = input("¿Desea cambiar el nombre del archivo? (Y/N): ").lower()
    
    temp = 0

    if respuesta == 'y' or respuesta == 'Y':
        # Cambia el nombre del archivo

        with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
            nuevo_nombre = nombre_file.read().strip()
            os.rename(pdf_path, nuevo_nombre)
        print(f"El nombre del archivo ha sido cambiado a: {nuevo_path}")

        temp = 1

    if(temp == 0):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information2(text,x)
        nombre = str (inpu[0:4] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        print (nombre)

        nuevo_path = "E:\CLINICA SANENS\Clinica sanens sem1\\"+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)

        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/N): ").lower()

        if respuesta == 'y' or respuesta == 'Y':
            # Cambia el nombre del archivo
            
            
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: {nuevo_path}")
    
if __name__ == "__main__":
    while(1):
        main()

