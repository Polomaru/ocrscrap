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

def extract_information(text, num_digits=8, keyword='PACIENTE:'):
    # Busca el primer número de num_digits dígitos
    match_numero = re.search(rf'\b\d{{{num_digits}}}\b', text)
    numero_digitos = match_numero.group() if match_numero else None

    lines = text.split('\n')
    
    # Busca la palabra keyword y obtiene las líneas siguientes hasta la próxima línea en blanco
    keyword_line = next((line for line in lines if keyword in line), None)
    
    if keyword_line:
        start_index = lines.index(keyword_line)
        next_blank_line = next((i for i, line in enumerate(lines[start_index + 1:]) if not line.strip()), None)
        
        if next_blank_line is not None:
            end_index = start_index + 1 + next_blank_line
            palabras_despues_keyword = ' '.join(lines[start_index + 1:end_index]).strip()
            return numero_digitos, palabras_despues_keyword
    
    return None, ''


def save_text_to_txt(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def main(inpu):
    pdf_path = 'E:\CLINICA SANENS\Clinica sanens sem1\\'+(inpu)+'.pdf'
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

    elif(respuesta == 'i'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,8,'PACIENTEI')
        nombre = str (inpu[0:5] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
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
        
    elif(respuesta == '9'):
        print("NOSECAMBIO")
        print()

        numero_8_digitos, palabras_despues_paciente = extract_information(text,9)
        nombre = str (inpu[0:5] +" "+ numero_8_digitos +" "+ palabras_despues_paciente)
        print (nombre)

        nuevo_path = "E:\CLINICA SANENS\Clinica sanens sem1\\"+nombre+".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)

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

