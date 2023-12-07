import re
def extract_information(text,num_digits=8, keyword='PACIENTE:'):
    match_numero = re.search(rf'\b\d{{{num_digits}}}\b', text)
    numero_digitos = match_numero.group() if match_numero else None

    x = ''
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if keyword in line:
            # Busca la próxima línea que no esté en blanco
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    # Imprime la información después de la keyword
                    x = (lines[j].strip())
                    break
    return numero_digitos, x
    # Si no se encuentra la keyword, imprimir un mensaje indicando que no se encontró

# Ejemplo de uso
texto_prueba = """HISTORIA CLIN CA N
' ° 45218078 — D.N.l.
PROCEDENCIA:
NO ESPECIFICA
PACIENTE:
ESPINOZA COLLADO GABRIELA
FECHA DE NACIMIENTO EDAD: SEXO:
31-05-1988 34 Años 11 Meses 23 Dias FEMENINO
FECHA DE INGRESO: CORRELATIVO LOLCLIQOOO
22-05-2023 0011851
ESTADO C|\/1L: TELEFONO: EMAIL:"""

print(extract_information(texto_prueba))
