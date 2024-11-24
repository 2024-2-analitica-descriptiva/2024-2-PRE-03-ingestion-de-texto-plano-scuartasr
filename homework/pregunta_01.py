"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

def lectura_datos(direccion: str, encod: str) -> list:
    """
    Esta función realiza la lectura de unos datos que están en un archivo
    de texto plano
    """
    with open(direccion, 'r', encoding=encod) as file:
        archivo = file.readlines()

    return archivo

#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

def encontrar_segmentos(texto: str) -> list:
    """
    Esta función recibe un string e identifica los diferentes segmentos
    de texto, entendiendo como segmento de texto aquel que se encuentra
    rodeado por dos o más espacios en blanco o un tabulador (no separa
    si internamente se tiene solo un espacio entre palabra y palabra).
    Retorna una lista con las posiciones del primer caracter de cada
    segmento de texto
    """
    # Lista que almacenará las posiciones de texto
    posiciones = []

    # Banderas dentro de la iteración
    en_segmento = False
    inicio_segmento = None
    espacios_consecutivos = 0

    # Iterando en la cadena de texto, conservando el índice y el elemento
    for indice, elemento in enumerate(texto):
        if elemento in (' ', '\t'):  # Contamos los espacios/tabulaciones consecutivos
            espacios_consecutivos += 1
        else:
            # Si hay más de un espacio consecutivo y no nos encontramos en un
            # segmento de texto...
            if espacios_consecutivos > 1 and en_segmento:
                # ... guardamos la posición, porque es la primera de un segmento  
                posiciones.append(inicio_segmento)
                en_segmento = False

            espacios_consecutivos = 0  # Reiniciamos el contador de espacios

            if not en_segmento:  # Iniciamos un nuevo segmento
                inicio_segmento = indice
                en_segmento = True

    if en_segmento:  # Si hay un segmento abierto al final del texto
        posiciones.append(inicio_segmento)

    return posiciones

#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

def combinar_strings(string1: str, string2: str) -> list:
    """
    Toma los elementos de dos listas distintas y devuelve una única lista
    con un resultado coherente
    """
    
    posiciones1 = encontrar_segmentos(string1)
    posiciones2 = encontrar_segmentos(string2)
    resultado = []
    
    # Iterar sobre las posiciones de la primera lista
    for i, pos1 in enumerate(posiciones1):
        # Obtener el fragmento de string1 correspondiente a la posición
        if i + 1 < len(posiciones1):
            fragmento1 = string1[pos1:posiciones1[i + 1]].strip()
        else:
            fragmento1 = string1[pos1:].strip()

        # Verificar si la posición de string1 también está en posiciones2
        if pos1 in posiciones2:
            # Encontrar la posición en string2 correspondiente
            j = posiciones2.index(pos1)
            if j + 1 < len(posiciones2):
                fragmento2 = string2[posiciones2[j]:posiciones2[j + 1]].strip()
            else:
                fragmento2 = string2[posiciones2[j]:].strip()
            
            # Concatenar fragmento1 con fragmento2
            fragmento1 = f"{fragmento1} {fragmento2}"
        
        # Agregar el fragmento resultante alb resultado
        resultado.append(fragmento1)
    
    return resultado

#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________
def mejoramiento_titulo(cabeceras: list) -> list:
    """
    Esta función recibe una lista con el nombre de las variables de un marco de
    datos y las regresa en un formato 'tidy'
    """
    
    # Se chequea si existe algún elemento vacío
    retorno = [x.replace(' ', '_').lower() for x in cabeceras if x.strip() != ""]

    return retorno
#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

def division_filas(lineas: list, header: list) -> pd.DataFrame:
    """
    Esta función toma cada una de las lineas de contenido de una tabla como una lista,
    junto con otra lista asociada a la cabecera de la información. Lo que hace es
    asignar de forma adecuada cada línea de un texto plano a su respectiva fila
    """
    # Inicializar variables para almacenar resultados
    rows = []
    current_row = []

    # Procesar cada línea del archivo
    for line in lineas:
        stripped_line = line.strip()  # Eliminar espacios en blanco iniciales y finales
        if stripped_line:  # Si la línea no está vacía
            # Detectar si es una nueva fila (basado en el número inicial)
            if re.match(r'^\d+\s+', stripped_line):
                # Si ya hay una fila en curso, guardar la actual
                if current_row:
                    rows.append(current_row)
                # Iniciar una nueva fila
                current_row = [stripped_line]
            else:
                # Continuar agregando líneas al contenido de la fila actual
                if current_row:
                    current_row[-1] += " " + stripped_line
        else:
            # Si la línea está vacía, cerrar la fila actual
            if current_row:
                rows.append(current_row)
                current_row = []

    # Asegurarse de guardar la última fila en curso
    if current_row:
        rows.append(current_row)

    # Procesar cada fila para dividir en columnas
    processed_data = []
    for row in rows:
        full_text = " ".join(row)  # Unir todas las líneas de la fila
        # Separar en columnas basadas en el patrón esperado
        match = re.match(r'^(\d+)\s+(\d+)\s+([\d,]+ %)\s+(.*)$', full_text)
        if match:
            processed_data.append(match.groups())

    # Crear un DataFrame a partir de los datos procesados
    df = pd.DataFrame(processed_data, columns=header)
    df.to_csv("./files/output/output.csv", index=False)

    return df

def exceso_espacios(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Esta función recibe un marco de datos df y se eliminan los
    excesos de espacios que pueda tener la columna col
    """
    df[col] = df[col].str.strip()
    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
    df.to_csv("./files/output/output.csv", index=False)
    return df

#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

def eliminacion_signos(df: pd.DataFrame, col: str, signo: str) -> pd.DataFrame:
    """
    Esta función toma una columna col de un marco de datos df y eliminar
    cualquier ocurrencia del signo signo y convierte la columna en tipo
    flotante
    """

    df[col] = df[col].str.replace(signo, '')

    df[col] = df[col].str.replace(',', '.').astype(float)
    df.to_csv("./files/output/output.csv", index=False)

    return df

def adicion_saltos(df: pd.DataFrame, col: str, patron: str) -> pd.DataFrame:
    """
    Esta agregar saltos de página cada que se encuentra el patrón patron en la
    columna col del marco de datos df
    """  

    df[col] = df[col].str.replace(", ", ", \n")


    return df

#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________
#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________
#
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """

    direccion = './files/input/clusters_report.txt'
    df = lectura_datos(direccion, encod='utf-8')

    df2 = pd.read_fwf(direccion)

    # Selección de los encabezados
    header = df[:2]

    header = combinar_strings(header[0], header[1])

    header = mejoramiento_titulo(header)

    df = division_filas(lineas=df[4:], header=header)

    df = exceso_espacios(df, df.columns[3])

    df = eliminacion_signos(df=df, col=df.columns[2], signo=' %')

    # Conversión de algunas columnas a tipo numérico
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace(".", "")

    return df

print(pregunta_01())
