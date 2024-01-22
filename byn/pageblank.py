import fitz  # PyMuPDF
from PIL import Image, ImageFilter
import os

def convert_to_bw(input_pdf, output_folder, dpi=100):
    # Abre el archivo PDF
    pdf_document = fitz.open(input_pdf)

    # Crear el directorio de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Inicializar lista para almacenar porcentajes y nombres de cada página
    page_info_list = []

    for page_num in range(pdf_document.page_count):
        # Obtiene la página
        page = pdf_document[page_num]

        # Convierte la página a imagen
        image = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))

        # Crea una imagen Pillow desde la imagen PyMuPDF
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Aplicar filtro de suavizado
        smooth_image = pil_image.filter(ImageFilter.SMOOTH)

        # Ajustar umbral de conversión a blanco y negro
        threshold = 200  # Ajusta este valor según sea necesario
        bw_image = smooth_image.convert("L").point(lambda x: 0 if x < threshold else 255, '1')

        # Calcula el porcentaje de blanco y negro
        white_percentage, _ = calculate_color_percentages(bw_image)

        # Almacena información de la página
        page_info_list.append((page_num + 1, white_percentage))

    # Filtra las páginas con porcentaje de blanco mayor al 98%
    filtered_pages = [(page, white_percentage) for page, white_percentage in page_info_list if white_percentage > 99.8]

    # Guarda la información en un archivo .txt
    output_txt_path = os.path.join(output_folder, "borrar.txt")
    with open(output_txt_path, 'w', encoding='utf-8') as delete_file:
        for page_num, _ in filtered_pages:
            delete_file.write(str(page_num) + ",")

    return output_folder

def calculate_color_percentages(image):
    # Calcula el porcentaje de blanco y negro
    total_pixels = image.size[0] * image.size[1]
    white_pixels = sum(1 for pixel in image.getdata() if pixel == 255)
    black_pixels = total_pixels - white_pixels

    white_percentage = (white_pixels / total_pixels) * 100
    black_percentage = (black_pixels / total_pixels) * 100

    return white_percentage, black_percentage

def process_pdfs_in_folder(folder_path, output_folder, dpi=100, threshold=200, white_percentage_threshold=99.8):
    # Obtener la lista de archivos PDF en la carpeta
    pdf_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        # Construir la ruta completa del archivo PDF
        input_pdf = os.path.join(folder_path, pdf_file)

        # Convertir a blanco y negro y calcular porcentajes
        output_folder_for_pdf = os.path.join(output_folder, pdf_file.replace(".pdf", ""))
        convert_to_bw(input_pdf, output_folder_for_pdf, dpi=dpi, threshold=threshold, white_percentage_threshold=white_percentage_threshold)

    print("Proceso completado. Páginas a borrar listadas en los archivos 'borrar.txt' en las carpetas respectivas.")

def convert_folder_to_bw(input_folder, output_folder, dpi=100):
    # Crear el directorio de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(input_folder, filename)

            # Abre el archivo PDF
            pdf_document = fitz.open(input_pdf)

            # Inicializar lista para almacenar porcentajes y nombres de cada página
            page_info_list = []

            for page_num in range(pdf_document.page_count):
                # Obtiene la página
                page = pdf_document[page_num]

                # Convierte la página a imagen
                image = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))

                # Crea una imagen Pillow desde la imagen PyMuPDF
                pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

                # Aplicar filtro de suavizado
                smooth_image = pil_image.filter(ImageFilter.SMOOTH)

                # Ajustar umbral de conversión a blanco y negro
                threshold = 200  # Ajusta este valor según sea necesario
                bw_image = smooth_image.convert("L").point(lambda x: 0 if x < threshold else 255, '1')

                # Calcula el porcentaje de blanco y negro
                white_percentage, _ = calculate_color_percentages(bw_image)

                # Almacena información de la página
                page_info_list.append((page_num + 1, white_percentage))

            # Filtra las páginas con porcentaje de blanco mayor al 98%
            filtered_pages = [(page, white_percentage) for page, white_percentage in page_info_list if white_percentage > 99.8]
            
            new_pdf_path = os.path.join(output_folder, f"C:\\Users\\riosv\\OneDrive\\Desktop\\New folder (2)\\BORRADO\{os.path.splitext(filename)[0]}.pdf")
            new_pdf_document = fitz.open()

            for page_num in range(pdf_document.page_count):
                # Si la página no está en filtered_pages, agrégala al nuevo PDF
                if page_num + 1 not in [page for page, _ in filtered_pages]:
                    new_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

            # Guarda el nuevo PDF
            new_pdf_document.save(new_pdf_path)
            new_pdf_document.close()

            print(f"Proceso completado para {filename}. Páginas a borrar excluidas. Nuevo PDF guardado en '{new_pdf_path}'.")


if __name__ == "__main__":
    input_folder = r'C:\Users\riosv\OneDrive\Desktop\New folder (2)'
    output_folder = "byn_resultados"

    # Convertir a blanco y negro, y calcular porcentajes para todos los archivos en la carpeta de entrada
    convert_folder_to_bw(input_folder, output_folder, dpi=100)

    print("Proceso completado para todos los archivos en la carpeta de entrada.")
