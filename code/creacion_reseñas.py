import pandas as pd
from sqlalchemy import create_engine
from .connection  import get_connection
import zipfile      
from .limpieza import extract_guest, extract_bathroom, extract_bed, extract_bedroom, extract_number_of_baths, extract_price


def extraer_datos_y_unir_2():
    """
    Función para extraer registros específicos de una tabla SQL según una lista de IDs y concatenarlos
    con otro DataFrame según la columna ID.

    Returns:
    - pd.DataFrame: DataFrame combinado con los registros seleccionados.
    """
    # Leer el archivo CSV `resultados_nlp.csv` para obtener la lista de IDs
    
    resultados_path = os.path.abspath('../objetos/resultados_nlp.csv')
    print("Ruta absoluta a 'resultados_nlp.csv':", resultados_path)
    
    try:
        resultados = pd.read_csv(resultados_path)
        lista_ids = resultados['id_url'].tolist()
        print("Archivo 'resultados_nlp.csv' cargado exitosamente.")
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'resultados_nlp.csv' en la ruta especificada.")



    # Definir las columnas que queremos cargar desde la base de datos o desde el CSV de respaldo
    columnas = ['id_url', 'title', 'price', 'type_host', 'complete_data_list', 'city', 'number_reviews']

    try:
        # Crear la conexión a la base de datos
        connection = get_connection()
        nombre_base_datos = 'nombre_base_datos'  # Reemplaza con el nombre de tu base de datos
        tabla = 'airbnb_listings_1'

        # Crear el motor de conexión SQL usando `get_connection` y `nombre_base_datos`
        engine = create_engine('mysql+pymysql://', creator=lambda: connection)

        # Generar la consulta SQL usando los IDs de la lista
        columnas_str = ', '.join(columnas)
        query = f"""
        SELECT {columnas_str}
        FROM {tabla}
        WHERE id_url IN ({', '.join(['%s'] * len(lista_ids))})
        """

        # Ejecutar la consulta SQL y cargar los datos en un DataFrame
        df = pd.read_sql(query, engine, params=tuple(lista_ids))

        # Cerrar la conexión al terminar
        engine.dispose()

    except Exception as e:
        print(f"Error de conexión o consulta SQL: {e}")
        try:
            # Intentar cargar solo las columnas especificadas desde 'Airbnb.csv'
            df = pd.read_csv('../objetos/Airbnb.csv', usecols=columnas)
            print("Datos cargados desde el archivo 'Airbnb.csv' con columnas específicas.")
        except FileNotFoundError:
            print("Error: No se encontró 'Airbnb.csv'. Intentando cargar desde 'Airbnb.zip'...")
            try:
                # Cargar el archivo CSV desde el ZIP, especificando las columnas deseadas
                with zipfile.ZipFile('../objetos/Airbnb.csv.zip', 'r') as zip_ref:
                    with zip_ref.open('Airbnb.csv') as file:
                        df = pd.read_csv(file, usecols=columnas)
                        print("Datos cargados desde 'Airbnb.csv' dentro de 'Airbnb.zip'.")
            except FileNotFoundError:
                print("Error: No se encontró 'Airbnb.zip'.")
                return None
    
    # Crear las nuevas columnas aplicando funciones de extracción
    df['number_guest'] = df['complete_data_list'].apply(extract_guest)
    df['number_bedroom'] = df['complete_data_list'].apply(extract_bedroom)
    df['number_beds'] = df['complete_data_list'].apply(extract_bed)
    df['type_bathroom'] = df['complete_data_list'].apply(extract_bathroom)
    df['number_bathroom'] = df['complete_data_list'].apply(extract_number_of_baths)
    df['price'] = df['price'].apply(extract_price)
    df.drop(columns='complete_data_list', inplace=True)

    # Convertir ambas columnas 'id_url' al mismo tipo de datos (string) para el merge
    resultados['id_url'] = resultados['id_url'].astype(str)
    df['id_url'] = df['id_url'].astype(str)

    # Unir el DataFrame `resultados` con el DataFrame de SQL en base a la columna 'id_url'
    df_reseñas = pd.merge(resultados, df, on='id_url', how='left')
    if 'Unnamed: 0' in df_reseñas.columns:
        df_reseñas.drop(columns='Unnamed: 0', inplace=True)

    return df_reseñas

extraer_datos_y_unir_2()
