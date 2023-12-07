def extract_information(text, keyword='PACIENTE:'):
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if keyword in line:
            # Encuentra la próxima línea en blanco
            for j in range(i + 1, len(lines)):
                if not lines[j].strip():
                    # Concatena las líneas desde la keyword hasta la línea en blanco
                    return ' '.join(lines[i + 1:j]).strip()
    
    return ''

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

palabras = extract_information(texto_prueba)
print("Palabras después de la palabra clave:", palabras)
