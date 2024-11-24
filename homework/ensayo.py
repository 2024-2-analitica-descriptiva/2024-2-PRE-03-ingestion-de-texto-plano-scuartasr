import re
import pandas as pd

# Ruta al archivo .txt
file_path = './files/input/clusters_report.txt'

# Leer todas las líneas del archivo
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

lines = lines[4:]

# Inicializar variables para almacenar resultados
rows = []
current_row = []

# Procesar cada línea del archivo
for line in lines:
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
df = pd.DataFrame(processed_data, columns=["ID", "Value", "Percentage", "Description"])

# Mostrar el DataFrame
print(df)

# Guardar el DataFrame en un archivo CSV si es necesario
df.to_csv("./files/output/output.csv", index=False)
