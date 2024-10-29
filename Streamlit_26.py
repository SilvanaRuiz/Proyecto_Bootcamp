import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from dotenv import load_dotenv
import os
from code.creacion_reseñas import extraer_datos_y_unir_2
from sklearn.preprocessing import OneHotEncoder
import pickle
import zipfile
from code.limpieza import limpiezadedatos
from scipy import stats

# Configurar la página
st.set_page_config(page_title="Análisis de Mercado de Airbnb", layout="wide")

# Estilos CSS personalizados
st.markdown(
    """
    <style>
    /* Fondo de la barra lateral en lavanda claro */
    .stSidebar {
        background-color: #E6E6FA !important;
    }
    """,
    unsafe_allow_html=True
)

try:
    # Intentar cargar el archivo CSV
    df = pd.read_csv('objetos/Airbnb.csv')
    print("Archivo CSV cargado exitosamente.")
except FileNotFoundError:
    print("Archivo 'Airbnb.csv' no encontrado. Intentando descomprimir 'Airbnb.csv.zip'...")

    # Intentar descomprimir el archivo zip
    try:
        with zipfile.ZipFile('objetos/Airbnb.csv.zip', 'r') as zip_ref:
            zip_ref.extractall('objetos')  # Extrae en la carpeta 'objetos'
        print("Archivo descomprimido exitosamente.")

        # Intentar cargar el CSV nuevamente después de descomprimir
        df = pd.read_csv('objetos/Airbnb.csv')
        print("Archivo CSV cargado exitosamente después de descomprimir.")

    except FileNotFoundError:
        print("Archivo 'Airbnb.csv.zip' no encontrado. Verifica que el archivo esté en el directorio.")
    except zipfile.BadZipFile:
        print("El archivo 'Airbnb.csv.zip' está dañado o no es un archivo ZIP válido.")

# Convertir el resultado de unique() a una lista
ciudades = df['city'].unique().tolist()
df_sin_na = df.dropna()
df_limpio = limpiezadedatos(df_sin_na)


def obtener_imagen_ciudad(city):
    """
    Función para obtener una imagen de una ciudad usando la API de Unsplash.
    """
     # Arma los headers con la clave de Unsplash desde st.secrets
    headers = {
        "Authorization": f"Client-ID {st.secrets['UNSPLASH_ACCESS_KEY']}",
        "Content-Type": "application/json"
    }
    
    # Agregar "city" al término de búsqueda para especificar que queremos una imagen de la ciudad
    query = f"{city} city"
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]
        else:
            st.write(f"No se encontraron imágenes para la ciudad: {city}")
            return None
    else:
        st.write("Error al conectarse a la API de Unsplash.")
        return None
   
def dashboard(df_limpio):
    st.title("🏠 Bienvenido a Airbnb Insights")

# Sección combinada de bienvenida y descripción de la app
    st.markdown("""
    <div style='background-color: #f5f5f5; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);'>
        <h2 style='color: #ab47bc; text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Descubre el Potencial de Airbnb en Tu Ciudad</h2>
        <p style='color: #424242; text-align: center; font-size: 16px; margin-top: 10px;'>Esta aplicación fue creada como proyecto fin de bootcamp de Hackaboss.</p>
        <p style='color: #424242; font-size: 15px; margin-top: 20px; line-height: 1.6;'>Con esta herramienta, podrás realizar un análisis exhaustivo del mercado de Airbnb, incluyendo:</p>
        <ul style='color: #424242; font-size: 15px; padding-left: 20px; line-height: 1.8;'>
            <li><b>Análisis Exploratorio de Datos</b>: Exploración de listados de Airbnb mediante <i>web scraping</i>.</li>
            <li><b>Análisis de Sentimiento de Reseñas</b>: Comparación de ratings de alojamientos con un análisis de sentimiento de las opiniones de los usuarios.</li>
            <li><b>Calculadora de Precios</b>: Predicción del precio adecuado para un Airbnb basado en la ciudad y características del alojamiento.</li>
        </ul>
        <p style='color: #424242; font-size: 15px; line-height: 1.6;'>A través de <b>web scraping</b>, hemos recopilado una amplia gama de información sobre múltiples ciudades. Esta información nos permite analizar diferentes aspectos del mercado, como las características de los alojamientos, las valoraciones de los huéspedes y las reseñas dejadas por los usuarios. Utilizando métodos de procesado de lenguaje natural como es el <b>análisis de sentimiento</b>, hemos utilizado las opiniones de los huéspedes para identificar patrones y obtener una comprensión profunda de lo que los usuarios valoran o critican en los alojamientos. Además, en base a los precios de los alojamientos en cada ciudad, hemos desarrollado una <b>calculadora predictiva de precios</b>. Esta herramienta analiza las tarifas actuales de Airbnb en una ciudad específica y, utilizando algoritmos de aprendizaje automático, estima el precio adecuado para tu alojamiento. Esta estimación no solo toma en cuenta las características de tu propiedad, sino que también se ajusta en función de los precios de otros alojamientos en la misma ciudad, brindándote una recomendación precisa y competitiva. Así, puedes asegurarte de que tu Airbnb esté alineado con el mercado local y maximizar tu ocupación y rentabilidad.</p>
    </div>
    """, unsafe_allow_html=True)


    st.title("📊 Dashboard de Airbnb Insights")

    # Obtener las ciudades únicas
    ciudades_unicas = df_limpio['city'].unique()

    # Sidebar para selección de ciudad
    st.sidebar.title("🏙️ Selecciona una ciudad")
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades_unicas)

    # Filtrar el DataFrame por la ciudad seleccionada
    df_ciudad = df_limpio[df_limpio['city'] == ciudad_seleccionada]

    # Obtener la URL de la imagen de la ciudad seleccionada
    imagen_url = obtener_imagen_ciudad(ciudad_seleccionada)

    # Calcular estadísticas principales
    total_alojamientos = len(df_ciudad)
    mean_rating = df_ciudad['rating'].mean()
    mean_price = df_ciudad['price'].mean()

    # Disposición en columnas para imagen y texto
    col1, col2 = st.columns([1, 2])  # La primera columna es más pequeña para la imagen, y la segunda es más amplia para el texto

    with col1:
        # Mostrar la imagen de la ciudad en la columna izquierda
        if imagen_url:
            st.image(imagen_url, caption=f"Vista de {ciudad_seleccionada}", use_column_width=True)

    with col2:
        # Contenedor principal del Dashboard en la columna derecha
        st.markdown("""
            <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                <h2 style='color: #ab47bc; text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Resumen de Datos de Airbnb</h2>
                <p style='color: #4a4a4a;'>Visualiza los principales indicadores de Airbnb en la ciudad seleccionada para tener una visión general del mercado.</p>
            </div>
            """, unsafe_allow_html=True)

        # Tarjetas de estadísticas principales con datos calculados
        st.markdown(f"""
            <div style='display: flex; gap: 20px; margin-top: 20px;'>
                <div style='flex: 1; background-color: #eaf4fc; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 24px; color: #1e3d59;'>🌆 Ciudad Seleccionada</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>{ciudad_seleccionada}</p>
                </div>
                <div style='flex: 1; background-color: #f9f4f4; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 24px;color: #1e3d59;'>🏠 Total de Alojamientos</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>{total_alojamientos}</p>
                </div>
                <div style='flex: 1; background-color: #f4f9f4; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 24px;color: #1e3d59;'>⭐ Rating Promedio</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>{mean_rating:.1f}</p>
                </div>
                <div style='flex: 1; background-color: #fcf4e4; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 24px;color: #1e3d59;'>💶 Precio Promedio</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>€{mean_price:.2f}/noche</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        # Nueva sección después del Dashboard
    st.title("🔄 Actualización de Datos de Airbnb")

    # Explicación sobre el proceso de Web Scraping
    st.markdown("""
    <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;'>
        <h2 style='color: #ab47bc; text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Actualización de Datos mediante Web Scraping</h2>
        <p style='color: #4a4a4a; line-height: 1.6;'>
            Dado que el proceso de web scraping puede llevar más de 2 horas debido a la cantidad de datos que se recopilan, no ha sido posible incluirlo directamente en esta aplicación.
        </p>
        <p style='color: #4a4a4a; line-height: 1.6;'>
            Si deseas realizar un nuevo scraping para obtener datos actualizados de una ciudad en particular, puedes descargar el script correspondiente.
            Solo necesitas especificar la ciudad y el país de tu interés, y el script se encargará de recopilar los datos más recientes de Airbnb.
        </p>
    </div>
    """, unsafe_allow_html=True)
    #Botón para descargar scrapping
    with open("code/scraping.py", "rb") as file:
        st.download_button(
            label="📥 Descargar Script de Web Scraping",
            data=file,
            file_name="scraping.py",
            mime="text/x-python"  # MIME específico para archivos .ipynb
        )

def analis_exploratorio():

    # Configuración de estilos
    sns.set(style="whitegrid")  # Fondo claro
   

    # Título
    st.markdown("<h1 style='text-align: center; color: #ab47bc;'>Visualización de Datos de Airbnb</h1>", unsafe_allow_html=True)


    # Selector de ciudad
    ciudades = df_limpio['city'].unique().tolist()
    st.sidebar.title("🏙️ Selecciona una ciudad")
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades)


    # Filtrar el DataFrame por la ciudad seleccionada
    df_ciudad = df_limpio[df_limpio['city'] == ciudad_seleccionada]

    # Caja de información general
    st.markdown(f"""
    <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
        <h2 style='text-align: center; color: #333333; font-weight: bold;'>Información General</h2>
        <p style='color: #4a4a4a; line-height: 1.6;'>
            
Esta sección te permite explorar información sobre los alojamientos de Airbnb mediante gráficos que analizan distintos aspectos del mercado en la ciudad seleccionada.
        </p>
        <p style='color: #4a4a4a; line-height: 1.6;'>
            <b>Histogramas y gráficos de barras:</b> Estos gráficos revelan la distribución de valores en cada variable, facilitando la identificación de distribuciones normales, sesgos, valores atípicos y asimetrías.
        </p>
        <p style='color: #4a4a4a; line-height: 1.6;'>
            <b>Gráficos de calor:</b> Visualizan la relación entre variables mediante colores, facilitando la detección de patrones, correlaciones y tendencias en los datos.
""", unsafe_allow_html=True)

    #######################################################################

    # Nueva paleta de colores
    palette = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948']

    # Crear pestañas para los gráficos
    tabs = st.tabs([
        "Distribución de Calificación",
        "Distribución de Precio",
        "Distribución de Precio por Tipo de Anfitrión",
        "Relación entre Precio y Calificación",
        "Distribución del Tiempo de Hospedaje",
        "Relación entre Tiempo de Hospedaje y Precio",
        "Mapa de Calor de Correlación entre Variables"
    ])

    # Distribución de Calificación
    with tabs[0]:
        st.header("Distribución de Calificación")
        st.markdown("Este gráfico muestra la distribución de las calificaciones de los alojamientos en la plataforma.")
        plt.figure(figsize=(10, 6))
        sns.histplot(df_ciudad['rating'], kde=True, bins=20, color=palette[2], edgecolor='black')
        sns.kdeplot(df_ciudad['rating'], color=palette[1], lw=2.5)
        plt.title('Distribución de Calificación', fontsize=18, weight='bold', color=palette[2])
        plt.xlabel('Rating', fontsize=14)
        plt.ylabel('Frecuencia', fontsize=14)
        st.pyplot(plt.gcf())

    # Distribución de Precio
    with tabs[1]:
        st.header("Distribución de Precio")
        st.markdown("Este gráfico muestra la distribución de los precios, resaltando la media para ver la tendencia general.")
        plt.figure(figsize=(10, 6))
        sns.histplot(df_ciudad['price'], kde=True, bins=20, color=palette[3], edgecolor='black')
        mean_price = df_ciudad['price'].mean()
        plt.axvline(mean_price, color=palette[1], linestyle='--', lw=2)
        plt.title('Distribución de Precio', fontsize=18, weight='bold', color=palette[3])
        plt.xlabel('Precio', fontsize=14)
        plt.ylabel('Frecuencia', fontsize=14)
        st.pyplot(plt.gcf())

    # Distribución de Precio por Tipo de Anfitrión
    with tabs[2]:
        st.header("Distribución de Precio por Tipo de Anfitrión")
        st.markdown("Este gráfico ilustra la variación de precios por categoría de anfitrión, destacando la dispersión de precios en cada tipo.")
        plt.figure(figsize=(10, 7))
        sns.violinplot(x='type_host', y='price', data=df_ciudad, inner=None, palette=palette)
        sns.swarmplot(x='type_host', y='price', data=df_ciudad, color='black', alpha=0.6)
        plt.title('Distribución de Precio por Tipo de Anfitrión', fontsize=18, weight='bold', color=palette[1])
        plt.xlabel('Tipo de Anfitrión', fontsize=14)
        plt.ylabel('Precio', fontsize=14)
        st.pyplot(plt.gcf())

    # Relación entre Precio y Calificación
    with tabs[3]:
        st.header("Relación entre Precio y Calificación")
        st.markdown("Este gráfico hexbin muestra la relación entre el precio y la calificación de los alojamientos.")
        plt.figure(figsize=(10, 7))
        plt.hexbin(df_ciudad['price'], df_ciudad['rating'], gridsize=30, cmap='YlGnBu', mincnt=1)
        plt.colorbar(label='Frecuencia')
        plt.title('Relación entre Precio y Calificación', fontsize=18, weight='bold')
        plt.xlabel('Precio', fontsize=14)
        plt.ylabel('Calificación', fontsize=14)
        st.pyplot(plt.gcf())

    # Distribución del Tiempo de Hospedaje
    with tabs[4]:
        st.header("Distribución del Tiempo de Hospedaje")
        st.markdown("Este gráfico presenta la distribución de tiempo de hospedaje, con una línea que marca la mediana.")
        plt.figure(figsize=(10, 6))
        sns.histplot(df_ciudad['hosting_time'], kde=True, bins=20, color=palette[4], edgecolor='black')
        median_time = df_ciudad['hosting_time'].median()
        plt.axvline(median_time, color=palette[1], linestyle='--', lw=2)
        plt.title('Distribución del Tiempo de Hospedaje', fontsize=18, weight='bold', color=palette[4])
        plt.xlabel('Meses de Hospedaje', fontsize=14)
        plt.ylabel('Frecuencia', fontsize=14)
        st.pyplot(plt.gcf())

    # Relación entre Tiempo de Hospedaje y Precio
    with tabs[5]:
        st.header("Relación entre Tiempo de Hospedaje y Precio")
        st.markdown("Este gráfico muestra cómo se relaciona el tiempo de experiencia del anfitrión con el precio.")
        plt.figure(figsize=(10, 7))
        sns.regplot(x='hosting_time', y='price', data=df_ciudad, scatter_kws={'color': palette[5]}, line_kws={'color': 'crimson'}, ci=95)
        plt.title('Relación entre Tiempo de Hospedaje y Precio', fontsize=18, weight='bold', color='crimson')
        plt.xlabel('Tiempo de Hospedaje (Meses)', fontsize=14)
        plt.ylabel('Precio', fontsize=14)
        st.pyplot(plt.gcf())

    # Mapa de Calor de Correlación entre Variables
    with tabs[6]:
        st.header("Mapa de Calor de Correlación entre Variables Numéricas")
        st.markdown("Este heatmap muestra la correlación entre las distintas variables numéricas del conjunto de datos.")
        plt.figure(figsize=(12, 10))
        sns.heatmap(df_ciudad[['rating', 'number_reviews', 'hosting_time', 'price', 'guest_favorite']].corr(), annot=True, cmap='coolwarm', linewidths=0.5, fmt=".2f")
        plt.title('Mapa de Calor de Correlación', fontsize=20, weight='bold')
        st.pyplot(plt.gcf())


def analisis_resenas():
    """
    Función para mostrar un análisis de las predicciones frente a los valores reales en Streamlit,
    mostrando el título de cada Airbnb individualmente con sus tablas respectivas.
    """
    st.markdown("<h1 style='text-align: center; color: #ab47bc;'>Análisis de Sentimiento en Reseñas de Airbnb</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='display: flex; justify-content: center;'>
        <p style='color: #ff9800; font-size: 16px; display: flex; align-items: center;'>
            <span style='font-size: 20px;'>⚠️</span>
            <span style='margin-left: 10px;'>Nota: Los resultados presentados se han calculado previamente para optimizar el rendimiento de la aplicación.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Caja gris para la descripción de la sección
    st.markdown("""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
           <h2 style='text-align: center; color: #333333; font-weight: bold;'>Exploración de Opiniones y Valoraciones de Usuarios</h2>
            <p style='color: #4a4a4a; line-height: 1.6;'>
                En esta sección, podrás explorar en profundidad el análisis de reseñas de usuarios en Airbnb. Utilizando técnicas de <b>análisis de sentimiento</b>, hemos evaluado las opiniones y valoraciones de los huéspedes en función de sus comentarios.
            </p>
            <p style='color: #4a4a4a; line-height: 1.6;'>
                Nuestro enfoque se centra en comparar las calificaciones de los alojamientos con los resultados del análisis de sentimiento de las reseñas. De esta manera, puedes visualizar la alineación (o discrepancia) entre las opiniones textuales de los huéspedes y las puntuaciones que otorgan. 
            </p>
        </div>
    """, unsafe_allow_html=True)
    # Extraer los datos
    predicciones_df = extraer_datos_y_unir_2()

    # Obtener las ciudades únicas
    ciudades_unicas = predicciones_df['city'].unique()

    # Sidebar para selección de ciudad
    st.sidebar.title("🏙️ Selecciona una ciudad")
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades_unicas)

    # Obtener la URL de la imagen de la ciudad seleccionada
    imagen_url = obtener_imagen_ciudad(ciudad_seleccionada)

    # Mostrar la imagen de la ciudad seleccionada en la parte superior
    if imagen_url:
        st.image(imagen_url, caption=f"Vista de {ciudad_seleccionada}", use_column_width=True)

    # Filtrar el DataFrame por ciudad seleccionada
    df_ciudad = predicciones_df[predicciones_df['city'] == ciudad_seleccionada].head(2)

    # Función para crear una tabla HTML sin índice
    def create_table_html(data):
        table_html = "<table style='width:100%; border-collapse: collapse;'>"
        # Header
        table_html += "<thead><tr style='background-color: #f5f5f5;'>"
        for col in data.columns:
            table_html += f"<th style='border: 1px solid #e0e0e0; padding: 8px; font-weight: bold;'>{col}</th>"
        table_html += "</tr></thead>"
        # Rows
        table_html += "<tbody>"
        for _, row in data.iterrows():
            table_html += "<tr>"
            for cell in row:
                table_html += f"<td style='border: 1px solid #e0e0e0; padding: 8px;'>{cell}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"
        return table_html

    # Mostrar cada Airbnb en un expander ocupando el ancho completo
    for idx, row in df_ciudad.iterrows():
        with st.expander(f"{row['title']}"):
            # Título grande dentro del expander
            st.markdown(f"<h3 style='font-size: 24px; margin: 0;'>{row['title']}</h3>", unsafe_allow_html=True)

            # Títulos de las secciones con tamaño de fuente reducido
            st.markdown("<h4 style='font-size: 18px;'>Calificación y Predicción</h4>", unsafe_allow_html=True)
            # Tabla de calificación y predicción (sin índice usando HTML directo)
            tabla_pred = pd.DataFrame({
                "Rating Real": [row['Valor Real']],
                "Predicción NLP": [row['Predicción']]
            })
            st.markdown(create_table_html(tabla_pred), unsafe_allow_html=True)

            st.markdown("<h4 style='font-size: 18px;'>Características del Alojamiento</h4>", unsafe_allow_html=True)
            # Tabla de características del alojamiento con iconos y colores condicionales (sin índice usando HTML directo)
            tabla_caracteristicas = pd.DataFrame({
                "Precio": [f"€{int(row['price'])}"],
                "Tipo de Huésped": ["👤 Superhost" if row['type_host'] == "Superhost" else "👤 Host"],
                "Número de Reseñas": [int(row['number_reviews'])],
                "Número de Huéspedes": [f"👥 {int(row['number_guest'])}"],
                "Número de Habitaciones": [f"🛌 {int(row['number_bedroom'])}"],
                "Número de Camas": [f"🛏️ {int(row['number_beds'])}"],
                "Tipo de Baño": [row['type_bathroom']],
                "Número de Baños": [f"🚽 {int(row['number_bathroom'])}"]
            })
            st.markdown(create_table_html(tabla_caracteristicas), unsafe_allow_html=True)







def modelo_prediccion():
    # Encabezado principal 
    st.markdown("<h1 style='text-align: center; color: #ab47bc;'>Modelo de Predicción de Precios de Airbnb</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7B7D7D;'>Obtén una estimación del rango de precios para tu alojamiento</h3>", unsafe_allow_html=True)
    

    st.markdown("""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h2 style='text-align: center;color: #333333; font-weight: bold;'>Estimación de Precios de Alojamientos en Airbnb</h2>
            <p style='color: #4a4a4a; line-height: 1.6;'>
                Esta sección permite estimar el rango de precios de alojamientos en función de características específicas (como ciudad, tipo de baño, número de habitaciones y capacidad de huéspedes). Utiliza técnicas de <b>aprendizaje automático</b> para analizar los datos históricos de Airbnb y, a través de modelos de clasificación y regresión, determina patrones y relaciones en las características de los alojamientos.
            </p>
            <p style='color: #4a4a4a; line-height: 1.6;'>
                Primero, asigna cada alojamiento a un clúster específico para reflejar mejor sus características y, luego, aplica un modelo de regresión optimizado para estimar el precio y su rango probable. Esto permite obtener una predicción más precisa y personalizada para cada alojamiento, asegurando que el precio esté alineado con la competencia local.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Texto de instrucciones con margen superior para mayor separación
    st.markdown("<p style='color: #7B7D7D; margin-top: 20px;'>Completa los detalles de tu alojamiento para obtener una estimación de precio.</p>", unsafe_allow_html=True)
    
    # Cargar el modelo de clasificación entrenado
    with open('./objetos/modelo_clasificacion.pkl', 'rb') as file:
        modelo_clasificacion = pickle.load(file)
    
    # Cargar los modelos de regresión entrenados para cada clúster
    with open('./objetos/modelo_c0.pkl', 'rb') as file:
        modelo_c0 = pickle.load(file)
    with open('./objetos/modelo_c1.pkl', 'rb') as file:
        modelo_c1 = pickle.load(file)
    with open('./objetos/modelo_c2.pkl', 'rb') as file:
        modelo_c2 = pickle.load(file)
    
    # Cargar los percentiles del error absoluto para cada modelo
    with open('./objetos/percentiles_modelo0.pkl', 'rb') as file:
        percentil_inferior0, percentil_superior0 = pickle.load(file)
    with open('./objetos/percentiles_modelo1.pkl', 'rb') as file:
        percentil_inferior1, percentil_superior1 = pickle.load(file)
    with open('./objetos/percentiles_modelo2.pkl', 'rb') as file:
        percentil_inferior2, percentil_superior2 = pickle.load(file)

    # Cargar los encoders y columnas
    with open('./objetos/encoder_city.pkl', 'rb') as file:
        encoder_city = pickle.load(file)
    with open('./objetos/city_columns.pkl', 'rb') as file:
        city_columns = pickle.load(file)
    with open('./objetos/encoder_bathroom.pkl', 'rb') as file:
        encoder_bathroom = pickle.load(file)
    with open('./objetos/bathroom_columns.pkl', 'rb') as file:
        bathroom_columns = pickle.load(file)
    with open('./objetos/columnas_X.pkl', 'rb') as file:
        columnas_X = pickle.load(file)

   
   
    # Seleccionar las ciudades desde el DataFrame
    ciudades = df['city'].unique()
    st.sidebar.title("🏙️ Selecciona una ciudad")
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades)
    #city = st.selectbox("📍 Ciudad", ciudades, help="Selecciona la ciudad de tu alojamiento")
    type_bathroom = st.selectbox("🛁 Tipo de baño", ["private", "shared"], help="Selecciona el tipo de baño")
    number_bedroom = st.number_input("🛌 Número de habitaciones", min_value=0, step=1, help="Especifica la cantidad de habitaciones")
    number_beds = st.number_input("🛏️ Número de camas", min_value=0, step=1, help="Especifica el número de camas disponibles")
    number_guest = st.number_input("👥 Número de huéspedes", min_value=1, step=1, help="Indica la capacidad máxima de huéspedes")
    
    # Espacio visual y botón estilizado
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Calcular Rango de Precios"):
        # Crear un DataFrame con los datos del usuario
        nuevos_datos = {
            "city": [ciudad_seleccionada],
            "type_bathroom": [type_bathroom],
            "number_bedroom": [number_bedroom],
            "number_beds": [number_beds],
            "number_guest": [number_guest]
        }
        df_nuevos_datos = pd.DataFrame(nuevos_datos)

        # Aplicar las transformaciones de One-Hot Encoding
        city_encoded = encoder_city.transform(df_nuevos_datos[['city']]).toarray()
        city_df = pd.DataFrame(city_encoded, columns=city_columns)
        
        bathroom_encoded = encoder_bathroom.transform(df_nuevos_datos[['type_bathroom']]).toarray()
        bathroom_df = pd.DataFrame(bathroom_encoded, columns=bathroom_columns)

        # Combinar todas las columnas
        df_nuevos_datos = pd.concat([df_nuevos_datos.reset_index(drop=True), city_df, bathroom_df], axis=1)
        df_nuevos_datos = df_nuevos_datos.reindex(columns=columnas_X, fill_value=0)

        # **Paso 1**: Predecir el clúster usando el modelo de clasificación
        cluster_predicho = modelo_clasificacion.predict(df_nuevos_datos)[0]
        
        # **Paso 2**: Seleccionar el modelo de regresión adecuado y sus percentiles
        if cluster_predicho == 0:
            modelo_regresion = modelo_c0
            percentil_superior = percentil_superior0
            percentil_inferior = percentil_inferior0
        elif cluster_predicho == 1:
            modelo_regresion = modelo_c1
            percentil_superior = percentil_superior1
            percentil_inferior = percentil_inferior1
        elif cluster_predicho == 2:
            modelo_regresion = modelo_c2
            percentil_superior = percentil_superior2
            percentil_inferior = percentil_inferior2
        else:
            st.error("Error: Clúster predicho no válido.")
            return  # Salir de la función si el clúster no es válido

        # **Paso 3**: Realizar la predicción con el modelo de regresión
        prediccion = modelo_regresion.predict(df_nuevos_datos)

        # Calcular el rango de precios usando los percentiles
        intervalo_inferior = prediccion[0] - percentil_superior
        intervalo_superior = prediccion[0] + percentil_superior

        # Mostrar el resultado 
    
        
        st.markdown(f"""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;'>
        <h3 style='text-align: center; color: #ab47bc;'>Precio estimado: €{prediccion[0]:.2f}</h3>
        <h4 style='text-align: center; color: #7B7D7D;'>Rango de precio estimado para su Airbnb: €{intervalo_inferior:.2f} - €{intervalo_superior:.2f}</h4>
        </div>
        """, unsafe_allow_html=True)



# Aplicación principal
def main():
  

    st.sidebar.title("Menú de Navegación")  # En lugar de "Índice"
    page = st.sidebar.selectbox("Selecciona una sección", ("Dashboard", "Análisis Exploratorio","Análisis de Reseñas", "Modelo de Predicción")) 



# Diseño del Dashboard
    if page == "Dashboard" :
        dashboard(df_limpio)

    elif page== "Análisis Exploratorio":
        analis_exploratorio()

    elif page == "Análisis de Reseñas":
        analisis_resenas()
  
    elif page == "Modelo de Predicción":
        modelo_prediccion()

if __name__ == "__main__":
    main()
