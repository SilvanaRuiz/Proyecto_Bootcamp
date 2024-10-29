import pandas as pd
import os
import zipfile
from sqlalchemy import create_engine
from .connection import get_connection
from .limpieza import extract_guest, extract_bathroom, extract_bed, extract_bedroom, extract_number_of_baths, extract_price

def extraer_datos_y_unir_2():
    """
    Función para extraer registros específicos de una tabla SQL según una lista de IDs y concatenarlos
    con otro DataFrame según la columna ID.

    Returns:
    - pd.DataFrame: DataFrame combinado con los registros seleccionados.
    """
    # Verifica la ruta a `resultados_nlp.csv`
    resultados_path = os.path.join(os.path.dirname(__file__), '../objetos/resultados_nlp.csv')
    print("Ruta absoluta a 'resultados_nlp.csv':", resultados_path)

    try:
        # Cargar `resultados_nlp.csv`
        resultados = pd.read_csv(resultados_path)
        lista_ids = resultados['id_url'].tolist()
        print("Archivo 'resultados_nlp.csv' cargado exitosamente.")
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'resultados_nlp.csv' en la ruta especificada.")
        return None

    # Define las columnas necesarias
    columnas = ['id_url', 'title', 'price', 'type_host', 'complete_data_list', 'city', 'number_reviews']

    try:
        # Crear la conexión a la base de datos
        connection = get_connection()
        tabla = 'airbnb_listings_1'
        engine = create_engine('mysql+pymysql://', creator=lambda: connection)

        # Generar la consulta SQL
        columnas_str = ', '.join(columnas)
        query = f"""
        SELECT {columnas_str}
        FROM {tabla}
        WHERE id_url IN ({', '.join(['%s'] * len(lista_ids))})
        """
        df = pd.read_sql(query, engine, params=tuple(lista_ids))
        engine.dispose()
        print("Datos cargados desde la base de datos.")
    except Exception as e:
        print(f"Error de conexión o consulta SQL: {e}")

        try:
            # Cargar desde 'Airbnb.csv'
            df_path = os.path.join(os.path.dirname(__file__), '../objetos/Airbnb.csv')
            df = pd.read_csv(df_path, usecols=columnas)
            print("Datos cargados desde 'Airbnb.csv'.")
        except FileNotFoundError:
            print("Error: No se encontró 'Airbnb.csv'. Intentando cargar desde 'Airbnb.csv.zip'...")
            try:
                zip_path = os.path.join(os.path.dirname(__file__), '../objetos/Airbnb.csv.zip')
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    with zip_ref.open('Airbnb.csv') as file:
                        df = pd.read_csv(file, usecols=columnas)
                        print("Datos cargados desde 'Airbnb.csv' dentro de 'Airbnb.zip'.")
            except FileNotFoundError:
                print("Error: No se encontró 'Airbnb.csv.zip'.")
                return None
            except zipfile.BadZipFile:
                print("Error: 'Airbnb.csv.zip' está dañado o no es un archivo ZIP válido.")
                return None

    # Procesamiento de datos usando las funciones de `limpieza.py`
    df['number_guest'] = df['complete_data_list'].apply(extract_guest)
    df['number_bedroom'] = df['complete_data_list'].apply(extract_bedroom)
    df['number_beds'] = df['complete_data_list'].apply(extract_bed)
    df['type_bathroom'] = df['complete_data_list'].apply(extract_bathroom)
    df['number_bathroom'] = df['complete_data_list'].apply(extract_number_of_baths)
    df['price'] = df['price'].apply(extract_price)
    df.drop(columns='complete_data_list', inplace=True)

    # Convertir las columnas 'id_url' al tipo string para el merge
    resultados['id_url'] = resultados['id_url'].astype(str)
    df['id_url'] = df['id_url'].astype(str)

    # Unir los DataFrames
    df_reseñas = pd.merge(resultados, df, on='id_url', how='left')
    if 'Unnamed: 0' in df_reseñas.columns:
        df_reseñas.drop(columns='Unnamed: 0', inplace=True)

    return df_reseñas
