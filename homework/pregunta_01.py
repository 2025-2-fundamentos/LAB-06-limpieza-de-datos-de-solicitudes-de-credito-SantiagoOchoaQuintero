import pandas as pd
import os

def pregunta_01():
    # Leer el archivo CSV con separador ';' y usar la primera columna como índice
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0) 
    
    # Limpiar y normalizar las columnas de tipo texto
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].str.lower()             # Convertir a minúsculas
        df[column] = df[column].str.replace("_", " ")   # Reemplazar guiones bajos por espacio
        df[column] = df[column].str.replace("-", " ")   # Reemplazar guiones por espacio
        df[column] = df[column].str.replace(",", "")    # Eliminar comas
        df[column] = df[column].str.replace("$", "")    # Eliminar símbolo de dólar
        df[column] = df[column].str.replace(".00", "")  # Eliminar decimales innecesarios

    # Convertir columnas numéricas a los tipos adecuados
    df["monto_del_credito"] = df["monto_del_credito"].astype(float)  # Convertir a float
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)       # Convertir a entero
    
    # Normalizar la columna de fechas, intentando distintos formatos
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).combine_first(pd.to_datetime(
        df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce"
    ))
    
    # Eliminar filas duplicadas
    df = df.drop_duplicates()
    
    # Eliminar filas con valores faltantes
    df = df.dropna()
    
    # Crear la carpeta de salida si no existe
    os.makedirs("files/output", exist_ok=True)
    
    # Guardar el DataFrame limpio en un nuevo CSV
    df.to_csv(
        "files/output/solicitudes_de_credito.csv",
        columns=df.columns,
        index=False,
        encoding="utf-8",
        sep=";"
    )
