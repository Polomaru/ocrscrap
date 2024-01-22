import fitz
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import re
import os

def pdf_to_bw_image(pdf_path, page_number, resolution=600, contrast_factor=2.0):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number - 1)

    # Adjust the desired resolution
    zoom_factor = resolution / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))

    # Convert pixmap to image
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Adjust contrast
    enhancer = ImageEnhance.Contrast(image)
    image_contrasted = enhancer.enhance(contrast_factor)

    # Convert image to black and white
    image_bw = ImageOps.grayscale(image_contrasted)

    return image_bw

def ocr_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def extract_information(text, num_digits=8, y=1):
    match_numero = re.search(rf'\b\d{{{num_digits}}}\b', text)
    numero_digitos = match_numero.group() if match_numero else ''

    x = ''
    lines = text.split('\n')
    keywords = ["PACIENTE","RPACIENTE", "PACENTE", "PACIENTEI", "PACIENTEZ", "FPACIENTE", "IPACIENTE", "APACIENTE"]
    for i, line in enumerate(lines):
        line = re.sub(r'[^a-zA-Z ]', '', line)
        line = line.replace(" ", "").replace("  ", "")
        line = line.upper()
        for keyi in keywords:
            if keyi == line:
                # Find the next non-blank line
                for j in range(i + y, len(lines)):
                    if lines[j].strip():
                        # Print information after the keyword
                        x = (lines[j].strip())
                        break
                break 
    x = re.sub(r'[^a-zA-Z ]', '', x)

    t = x.split()
    x = ''
    for i in t:
        i = i.upper()
        if len(i) > 2 or i in ["DE", "LA", "DA", "FE", "JO", "JR", "LI"]:
            replacements = {
                "NUNEZ": "NUÑEZ",
                "ORDONEZ": "ORDOÑEZ",
                "PENA": "PEÑA",
                "ACUNA": "ACUÑA",
                "BRENA": "BREÑA",
                "ZUNIGA": "ZUÑIGA",
                "MUNOZ": "MUÑOZ",
                "MUNIZ": "MUÑIZ",
                "CASTANEDA": "CASTAÑEDA",
                "ORMENO": "ORMEÑO",
                "RUBINOS": "RUBIÑOS",
                "SALDANA": "SALDAÑA",
                "IBANEZ": "IBAÑEZ",
                "REANO": "REAÑO",
                "QUINONES": "QUIÑONES",
                "QUINONEZ": "QUIÑONEZ",
                "SUANA": "SUAÑA",
                "OCANA": "OCAÑA",
                "CARRENO" : "CARREÑO",
                "PATINO" : "PATIÑO",
                "DUENAS" : "DUEÑAS",
                "JESSENA" : "JESSEÑA",
                "AVENDANO" : "AVENDAÑO",
                "BRICENO" : "BRICEÑO",
                "ARGANDONA" : "ARGANDOÑA",
                "AZANA" : "AZAÑA",
                "LUDENA" : "LUDEÑA",
                "MUNANTE" : "MUÑANTE",
                "BOLANOS" : "BOLAÑOS",
                "VICUNA" : "VICUÑA",
                "ROMANA" : "ROMAÑA",
                "ANAZGO" : "AÑAZGO",
                "UCANA" : "UCAÑA",
                "COVENAS" : "COVEÑAS",
                "COBENAS" : "COBEÑAS",
                "YANEZ" : "YAÑEZ",
                "BOLANO" : "BOLAÑO",
                "CANARI" : "CAÑARI",
                "TUPINO" : "TUPIÑO",
                "BANOS" : "BAÑOS",
                "PINA" : "PIÑA",
            }
            x += replacements.get(i, i) + " "

    if(numero_digitos=="" and num_digits==8):
        return extract_information(text, 9)
    return numero_digitos, x.strip()

def save_text_to_txt(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def convert_pdf_to_image(pdf_path, image_output):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    width, height = page.mediabox_size

    x0, y0, x1, y1 = 0, 0, width, height // 2
    region = fitz.Rect(x0, y0, x1, y1)
    image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72), clip=region)

    image.save(image_output)
    pdf_document.close()

def main(input_file, t):
    path = r'C:\Users\riosv\OneDrive\Desktop\New folder (2)\\'
    pdf_path = path + input_file + '.pdf'
    page_number = 1
    resolution = 200
    contrast_factor = 1.5

    convert_pdf_to_image(pdf_path, "ps.png")

    image = pdf_to_bw_image(pdf_path, page_number, resolution, contrast_factor)
    text = ocr_from_image(image)

    numero_8_digitos, palabras_despues_paciente = extract_information(text)

    output_path = 'output.txt'
    save_text_to_txt(text, output_path)

    nombre = str(input_file[0:t] + " " + numero_8_digitos + " " + palabras_despues_paciente)
    nombre = nombre.replace("  ", " ").replace("   ", " ")
    print()
    print(nombre)

    nuevo_path = path + nombre + ".pdf"
    with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
        nombre_file.write(nuevo_path)

    print()
    respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
    
    respuesta = respuesta.lower()
    if respuesta in ['y', '']:
        nuevo_nombre = ""
        with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
            nuevo_nombre = nombre_file.read().strip()
            os.rename(pdf_path, nuevo_nombre)
        print()
        print("El nombre del archivo ha sido cambiado a:")
        print(nuevo_nombre)
    
    elif respuesta == '9':
        print("NOSECAMBIO")
        print()
        numero_8_digitos, palabras_despues_paciente = extract_information(text, 9)
        nombre = str(input_file[0:t] + " " + numero_8_digitos + " " + palabras_despues_paciente)
        nombre = nombre.replace("  ", " ")
        print(nombre)
        nuevo_path = path + nombre + ".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)
        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
        if respuesta in ['y', '']:
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: ")
            print(nuevo_path)
            print()
        else:
            print("repit")
            print()
            main(input_file, t)
    elif respuesta == 'p':
        print("NOSECAMBIO")
        print()
        numero_8_digitos, palabras_despues_paciente = extract_information(text, 8,-2)
        nombre = str(input_file[0:t] + " " + numero_8_digitos + " " + palabras_despues_paciente)
        nombre = nombre.replace("  ", " ")
        print(nombre)
        nuevo_path = path + nombre + ".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)
        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
        if respuesta in ['y', '']:
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: ")
            print(nuevo_path)
            print()
        else:
            print("repit")
            print()
            main(input_file, t)
    elif respuesta == '0':
        print("NOSECAMBIO")
        print()
        numero_8_digitos, palabras_despues_paciente = extract_information(text, 8,-2)
        nombre = str(input_file[0:t] + " " + numero_8_digitos + " " + palabras_despues_paciente)
        nombre = nombre.replace("  ", " ")
        print(nombre)
        nuevo_path = path + nombre + ".pdf"
        with open('nombre.txt', 'w', encoding='utf-8') as nombre_file:
            nombre_file.write(nuevo_path)
        respuesta = input("¿Desea cambiar el nombre del archivo? (Y/ i / 9 /2 /N): ").lower()
        if respuesta in ['y', '']:
            with open('nombre.txt', 'r', encoding='utf-8') as nombre_file:
                nuevo_nombre = nombre_file.read().strip()
                os.rename(pdf_path, nuevo_nombre)
            print(f"El nombre del archivo ha sido cambiado a: ")
            print(nuevo_path)
            print()
        else:
            print("repit")
            print()
            main(input_file, t)
    elif respuesta == 'r':
        print("repit")
        print()
        main(input_file, t)
    elif respuesta == '0':
        print("next")
    else:
        print("repit")
        print()
        main(input_file, t)

if __name__ == "__main__":
    archivo_nombres_sin_extension = "nombres_sin_extension.txt"
    t = int(input("N: "))
    while True:
        with open(archivo_nombres_sin_extension, 'r') as archivo:
            primer_fila = archivo.readline().strip()

        if not primer_fila:
            print("Fin del archivo. No hay más filas para procesar.")
            break

        main(primer_fila, t)

        with open(archivo_nombres_sin_extension, 'r') as archivo:
            lineas = archivo.readlines()

        with open(archivo_nombres_sin_extension, 'w') as archivo:
            archivo.writelines(lineas[1:])
