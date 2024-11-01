#Bibliotecas
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
import plotly.graph_objects as go


# Configurar la página
st.set_page_config(page_title="Airbnb Insights", page_icon="🏠", layout='wide')

# Estilos CSS personalizados
st.markdown(
    """
    <style>
    /* Fondo de la barra lateral en color salmón con transparencia */
    .stSidebar {
        background-color: rgba(255, 90, 95, 0.5) !important;
    }
    </style>
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

# Custom CSS to control icon size, color, and styling
st.sidebar.markdown(
    """
    <style>
    .linkedin-icon {
        width: 20px; /* Ajusta el tamaño del icono */
        height: 20px;
        vertical-align: middle;
        margin-right: 10px; /* Espacio entre el icono y el nombre */
    }
    .team-member {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .team-member a {
        text-decoration: none; /* Quita el subrayado del enlace */
        color: black; /* Cambia el color del texto a negro */
    }
    .member-name {
        font-style: italic; /* Pone el nombre en cursiva */
    }
    </style>
    """,
    unsafe_allow_html=True
)



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

def inicio():
    # Logo y título
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <img src='https://1000marcas.net/wp-content/uploads/2020/01/Airbnb-Logo.png' alt='Airbnb Logo' width='80'/>
            <h1 style='color: #FF5A5F; font-weight: bold; font-family: Arial, sans-serif; margin-top: 10px;'>Bienvenido a Airbnb Insights</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Contenedor principal de bienvenida y descripción

    st.markdown("""
    <div style='background-color: #f5f5f5; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);'>
        <h2 style='color: #FF5A5F;  text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Descubre el Potencial de Airbnb en Tu Ciudad</h2>
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


def dashboard(df_limpio,ciudad_seleccionada):

    st.title("📊 Dashboard de Airbnb Insights")

    # Obtener las ciudades únicas
    ciudades_unicas = df_limpio['city'].unique()

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
            <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                <h2 style='color: #FF5A5F; text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Resumen de Datos de Airbnb</h2>
                <p style='color: #4a4a4a;'>Visualiza los principales indicadores de Airbnb en la ciudad seleccionada para tener una visión general del mercado.</p>
            </div>
            """, unsafe_allow_html=True)

        # Tarjetas de estadísticas principales con datos calculados
        st.markdown(f"""
            <div style='display: flex; gap: 20px; margin-top: 20px;'>
                <div style='flex: 1; background-color: #eaf4fc; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 22px; color: #1e3d59;'>🌆 Ciudad Seleccionada</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>{ciudad_seleccionada}</p>
                </div>
                <div style='flex: 1; background-color: #f9f4f4; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 22px;color: #1e3d59;'>🏠 Total de Alojamientos</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>{total_alojamientos}</p>
                </div>
                <div style='flex: 1; background-color: #f4f9f4; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 22px;color: #1e3d59;'>⭐ Rating Promedio</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>{mean_rating:.1f}</p>
                </div>
                <div style='flex: 1; background-color: #fcf4e4; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
                    <h3 style='font-size: 22px;color: #1e3d59;'>💶 Precio Promedio</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #1e3d59;'>€{mean_price:.2f}/noche</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        # Nueva sección después del Dashboard
    st.title("🔄 Actualización de Datos de Airbnb")

    # Explicación sobre el proceso de Web Scraping
    st.markdown("""
    <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;'>
        <h2 style='color: #FF5A5F; text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Actualización de Datos mediante Web Scraping</h2>
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

def analis_exploratorio(ciudad_seleccionada):
    # Título
    st.markdown("<h1 style='text-align: center; color: #FF5A5F;'>Visualización de Datos de Airbnb</h1>", unsafe_allow_html=True)

    # Filtrar el DataFrame por la ciudad seleccionada
    df_ciudad = df_limpio[df_limpio['city'] == ciudad_seleccionada]

    # Caja de información general
    st.markdown(f"""
    <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
        <h2 style='text-align: center; color: #333333; font-weight: bold;'>Información General</h2>
        <p style='color: #4a4a4a; line-height: 1.6;'>
            Esta sección te permite explorar información sobre los alojamientos de Airbnb mediante gráficos que analizan distintos aspectos del mercado en la ciudad seleccionada.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Opciones de gráficos y selección
    chart_options = ["Distribución de Calificación", "Distribución de Precio", "Precio por Tipo de Anfitrión",
                     "Relación Precio-Calificación", "Tiempo de Hospedaje", "Mapa de Correlación", "3D Interactivo"]
    selected_chart = st.selectbox("Selecciona el gráfico que deseas ver:", chart_options)

    # Paleta de colores personalizada
    palette = ['#FF5A5F', '#FFB6B9', '#FF9AA2', '#F5F5F5']

    # Función para gráficos 2D
    def plot_chart(chart_type):
        if chart_type == "Distribución de Calificación":
            st.header("Distribución de Calificación")
            st.write("Este gráfico muestra la distribución de las calificaciones que reciben los alojamientos. Nos permite identificar la frecuencia de distintas calificaciones y observar la tendencia general de satisfacción de los huéspedes.")
            fig = px.histogram(df_ciudad, x='rating', nbins=20, color_discrete_sequence=[palette[0]])
            fig.update_layout(xaxis_title="Calificación", yaxis_title="Frecuencia")
            st.plotly_chart(fig)
    
        elif chart_type == "Distribución de Precio":
            st.header("Distribución de Precio")
            st.write("Este gráfico ilustra cómo se distribuyen los precios de los alojamientos en la ciudad. La línea punteada representa la media, ayudando a visualizar los precios predominantes y el rango de variación.")
            fig = px.histogram(df_ciudad, x='price', nbins=20, color_discrete_sequence=[palette[1]])
            fig.add_vline(x=df_ciudad['price'].mean(), line_dash="dash", line_color=palette[0], annotation_text="Media", annotation_position="top right")
            fig.update_layout(xaxis_title="Precio", yaxis_title="Frecuencia")
            st.plotly_chart(fig)
    
        elif chart_type == "Precio por Tipo de Anfitrión":
            st.header("Distribución de Precio por Tipo de Anfitrión")
            st.write("Aquí se muestra la variación de precios entre los distintos tipos de anfitriones. Es útil para entender si algunos tipos de anfitriones tienden a cobrar precios más altos o bajos.")
            fig = px.violin(df_ciudad, x='type_host', y='price', box=True, points="all", color_discrete_sequence=[palette[2]])
            fig.update_layout(xaxis_title="Tipo de Anfitrión", yaxis_title="Precio")
            st.plotly_chart(fig)
    
        elif chart_type == "Relación Precio-Calificación":
            st.header("Relación entre Precio y Calificación")
            st.write("Este gráfico explora la relación entre el precio y la calificación de cada alojamiento, categorizado por tipo de anfitrión. Nos ayuda a identificar si los alojamientos más caros suelen tener mejores calificaciones.")
            fig = px.scatter(df_ciudad, x='price', y='rating', color='type_host', hover_data=['number_reviews', 'hosting_time'], color_continuous_scale=px.colors.sequential.Peach)
            fig.update_layout(xaxis_title="Precio", yaxis_title="Calificación")
            st.plotly_chart(fig)
    
        elif chart_type == "Tiempo de Hospedaje":
            st.header("Distribución del Tiempo de Hospedaje")
            st.write("Este gráfico muestra la distribución del tiempo que los anfitriones han estado ofreciendo hospedaje. La línea punteada representa la mediana, lo cual facilita ver qué tan experimentados suelen ser los anfitriones.")
            fig = px.histogram(df_ciudad, x='hosting_time', nbins=20, color_discrete_sequence=[palette[2]])
            fig.add_vline(x=df_ciudad['hosting_time'].median(), line_dash="dash", line_color="red", annotation_text="Mediana", annotation_position="top right")
            fig.update_layout(xaxis_title="Años de Hospedaje", yaxis_title="Frecuencia")
            st.plotly_chart(fig)
    
    # Gráfico 3D Interactivo
    def plot_3d():
        # Eliminamos las columnas innecesarias
        df_ciudad.drop(columns=['url', 'id_url', 'unique_id', 'title', 'Unnamed: 0'], inplace=True, errors='ignore')
    
        # Diccionario para traducir los nombres de las columnas
        traduccion_columnas = {
            'city': 'Ciudad',
            'guest_favorite': 'Favorito del Cliente',
            'rating': 'Calificación',
            'number_reviews': 'Número de Reseñas',
            'type_host': 'Tipo de Anfitrión',
            'hosting_time': 'Tiempo de Hospedaje',
            'price': 'Precio',
            'all_reviews': 'Reseñas Totales',
            'number_guest': 'Número de Huéspedes',
            'number_bedroom': 'Número de Habitaciones',
            'number_beds': 'Número de Camas',
            'type_bathroom': 'Tipo de Baño',
            'number_bathroom': 'Número de Baños'
        }
    
        # Cambiamos los nombres de las columnas en el dataframe
        df_ciudad.rename(columns=traduccion_columnas, inplace=True)
    
        st.header("Gráfico 3D Interactivo")
        st.write("Este gráfico 3D interactivo permite visualizar la relación entre tres variables seleccionadas, junto con una variable de color. Facilita el análisis de tendencias y relaciones complejas entre múltiples variables.")
    
        # Configuración de los selectores para los ejes, utilizando los nombres en español
        x_axis = st.selectbox("Selecciona el eje X:", df_ciudad.columns, index=list(df_ciudad.columns).index('Calificación'))
        y_axis = st.selectbox("Selecciona el eje Y:", df_ciudad.columns, index=list(df_ciudad.columns).index('Precio'))
        z_axis = st.selectbox("Selecciona el eje Z:", df_ciudad.columns, index=list(df_ciudad.columns).index('Número de Reseñas'))
        color_option = st.selectbox("Selecciona la variable de color:", df_ciudad.columns)
    
        # Generación del gráfico 3D
        fig = px.scatter_3d(df_ciudad, x=x_axis, y=y_axis, z=z_axis, color=color_option,
                            size_max=18, opacity=0.8, color_continuous_scale=px.colors.sequential.Peach,
                            title=f'Relación entre {x_axis}, {y_axis}, y {z_axis}')
        
        st.plotly_chart(fig)
   
    # Mapa de Calor de Correlación
    def correlacion():
        df_ciudad.drop(columns='Unnamed: 0', inplace=True)
        st.header("Mapa de Calor de Correlación entre Variables")
        st.write("Este mapa de calor muestra la correlación entre diferentes variables del dataset. Ayuda a identificar relaciones lineales positivas o negativas entre variables clave, como precio, calificación, y popularidad.")
        
        correlacion = df_ciudad[['rating', 'number_reviews', 'hosting_time', 'price', 'guest_favorite']].corr().round(2)
        correlacion.columns = ['Calificación', 'Número de Reseñas', 'Tiempo de Alojamiento', 'Precio', 'Favorito del Cliente']
        correlacion.index = correlacion.columns
    
        fig = go.Figure(
            data=go.Heatmap(
                z=correlacion.values,
                x=correlacion.columns,
                y=correlacion.columns,
                colorscale='Peach',
                colorbar=dict(title="Correlación")
            )
        )
    
        for i in range(len(correlacion.columns)):
            for j in range(len(correlacion.columns)):
                fig.add_annotation(
                    x=correlacion.columns[i],
                    y=correlacion.columns[j],
                    text=str(correlacion.values[i][j]),
                    showarrow=False,
                    font=dict(color="black", size=12)
                )
    
        fig.update_layout(
            font=dict(color='#4a4a4a'),
            xaxis=dict(tickangle=-45),
            yaxis=dict(autorange="reversed"),
            width=800,
            height=800
        )
    
        with st.container():
            col1, col2, col3 = st.columns([0.5, 3, 0.5])  
            with col2:
                st.plotly_chart(fig, use_container_width=True)
  
    # Mostrar gráfico seleccionado
    if selected_chart == "3D Interactivo":
        plot_3d()
    elif selected_chart == "Mapa de Correlación":
        correlacion()
    else:
        plot_chart(selected_chart)


def create_table_html(data):
    table_html = "<table style='width:100%; border-collapse: collapse;'>"
    table_html += "<thead><tr style='background-color: #f5f5f5;'>"
    for col in data.columns:
        table_html += f"<th style='border: 1px solid #e0e0e0; padding: 8px; font-weight: bold;'>{col}</th>"
    table_html += "</tr></thead><tbody>"
    for _, row in data.iterrows():
        table_html += "<tr>"
        for cell in row:
            table_html += f"<td style='border: 1px solid #e0e0e0; padding: 8px;'>{cell}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    return table_html
def analisis_resenas(ciudad_seleccionada):
    """
    Función para mostrar un análisis de las predicciones frente a los valores reales en Streamlit,
    mostrando los alojamientos en estilo de tarjetas y tablas de predicción y características al seleccionar un alojamiento.
    """
    st.markdown("<h1 style='text-align: center; color: #FF5A5F;'>Análisis de Sentimiento en Reseñas de Airbnb</h1>", unsafe_allow_html=True)
    
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

    # Extraer los datos usando la función original
    predicciones_df = extraer_datos_y_unir_2()

    # Filtrar el DataFrame por ciudad seleccionada
    df_ciudad = predicciones_df[predicciones_df['city'] == ciudad_seleccionada].head(3)  # Puedes ajustar el número de resultados

    # Título para los alojamientos
    st.markdown("<h2 style='color: #333333;'>Alojamientos en la ciudad</h2>", unsafe_allow_html=True)

    # Mostrar los alojamientos en estilo de tarjeta
    for idx, row in df_ciudad.iterrows():
        st.markdown(
            f"""
            <div style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 10px;'>
                <h4 style='color: #FF5A5F; margin-bottom: 5px;'>{row['title']}</h4>
                <p style='color: #555;'>Ubicación: {ciudad_seleccionada}</p>
            </div>
            """, unsafe_allow_html=True
        )

        # Botón dentro de la tarjeta para desplegar detalles
        if st.button(f"Mostrar información", key=f"btn_{idx}"):
            # Tabla de calificación y predicción
            tabla_pred = pd.DataFrame({
                "Rating Real": [row['Valor Real']],
                "Predicción Análisis de Sentimiento": [round(row['Predicción'], 2)]
            })
            st.markdown("<h4 style='text-align: center;'>Calificación y Predicción</h4>", unsafe_allow_html=True)
            st.markdown(create_table_html(tabla_pred), unsafe_allow_html=True)

            # Modificación del tipo de baño
            tipo_bano = "Privado" if row['type_bathroom'] == "private" else "Compartido"

            # Tabla de características del alojamiento con el tipo de baño modificado
            tabla_caracteristicas = pd.DataFrame({
                "Precio": [f"€{int(row['price'])}"],
                "Tipo de Huésped": ["👤 Superhost" if row['type_host'] == "Superhost" else "👤 Host"],
                "Número de Reseñas": [int(row['number_reviews'])],
                "Número de Huéspedes": [f"👥 {int(row['number_guest'])}"],
                "Número de Habitaciones": [f"🛌 {int(row['number_bedroom'])}"],
                "Número de Camas": [f"🛏️ {int(row['number_beds'])}"],
                "Tipo de Baño": [tipo_bano],
                "Número de Baños": [f"🚽 {int(row['number_bathroom'])}"]
            })
            st.markdown("<h4 style='text-align: center;'>Características del Alojamiento</h4>", unsafe_allow_html=True)
            st.markdown(create_table_html(tabla_caracteristicas), unsafe_allow_html=True)

def modelo_prediccion(ciudad_seleccionada):
    # Encabezado principal
    st.markdown("<h1 style='text-align: center; color: #FF5A5F;'>Modelo de Predicción de Precios de Airbnb</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7B7D7D;'>Obtén una estimación del rango de precios para tu alojamiento</h3>", unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h2 style='text-align: center;color: #333333; font-weight: bold;'>Estimación de Precios de Alojamientos en Airbnb</h2>
            <p style='color: #4a4a4a; line-height: 1.6;'>
                Esta sección permite estimar el rango de precios de alojamientos en función de características específicas (como ciudad, tipo de baño, número de habitaciones y capacidad de huéspedes). Utiliza técnicas de <b>aprendizaje automático</b> para analizar los datos históricos de Airbnb y, a través de modelos de clasificación y regresión, determina patrones y relaciones en las características de los alojamientos.
            </p>
            <p style='color: #4a4a4a; line-height: 1.6;'>
               Para hacer la predicción, se emplean modelos de regresión supervisados pre-entrenados que estiman tanto el precio de cada alojamiento como su posible variación. Esta metodología permite generar predicciones precisas y personalizadas, ajustando el precio de manera óptima según las características específicas de cada alojamiento y asegurando su competitividad en el mercado local.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<p style='color: #7B7D7D; margin-top: 20px;'>Completa los detalles de tu alojamiento para obtener una estimación de precio.</p>", unsafe_allow_html=True)
    
    
    # Cargar el modelo de regresión entrenados para cada clúster
    with open('./objetos/modelo.pkl', 'rb') as file:
        modelo = pickle.load(file)
  
    # Cargar los percentiles del error absoluto 
    with open('./objetos/percentiles_modelo.pkl', 'rb') as file:
        percentil_inferior, percentil_superior = pickle.load(file)
    # Cargar el r2
    with open('./objetos/r2.pkl', 'rb') as file:
        r2 = pickle.load(file)
    

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


    # Campos de entrada
    type_bathroom = st.selectbox("🛁 Tipo de baño", ["Privado", "Compartido"], help="Selecciona el tipo de baño")
    number_bedroom = st.number_input("🛌 Número de habitaciones", min_value=0, step=1, help="Especifica la cantidad de habitaciones")
    number_beds = st.number_input("🛏️ Número de camas", min_value=0, step=1, help="Especifica el número de camas disponibles")
    number_guest = st.number_input("👥 Número de huéspedes", min_value=1, step=1, help="Indica la capacidad máxima de huéspedes")
    
    # Mostrar ciudad seleccionada debajo del número de huéspedes
    st.write(f"📍 Ciudad seleccionada: {ciudad_seleccionada}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Calcular Rango de Precios"):
        # Transformación para el tipo de baño a valores compatibles con el modelo
        type_bathroom_value = "private" if type_bathroom == "Privado" else "shared"

        # Crear DataFrame para el modelo
        nuevos_datos = {
            "city": [ciudad_seleccionada],
            "type_bathroom": [type_bathroom_value],
            "number_bedroom": [number_bedroom],
            "number_beds": [number_beds],
            "number_guest": [number_guest]
        }
        df_nuevos_datos = pd.DataFrame(nuevos_datos)

        # Aplicar transformaciones de One-Hot Encoding
        city_encoded = encoder_city.transform(df_nuevos_datos[['city']]).toarray()
        city_df = pd.DataFrame(city_encoded, columns=city_columns)
        
        bathroom_encoded = encoder_bathroom.transform(df_nuevos_datos[['type_bathroom']]).toarray()
        bathroom_df = pd.DataFrame(bathroom_encoded, columns=bathroom_columns)

        # Combinar todas las columnas
        df_nuevos_datos = pd.concat([df_nuevos_datos.reset_index(drop=True), city_df, bathroom_df], axis=1)
        df_nuevos_datos = df_nuevos_datos.reindex(columns=columnas_X, fill_value=0)


        # Realizar predicción
        prediccion = modelo.predict(df_nuevos_datos)
        intervalo_inferior = prediccion[0] - percentil_superior
        intervalo_superior = prediccion[0] + percentil_superior

        # Mostrar resultado
        st.markdown(f"""
    <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;'>
        <h3 style='text-align: center; color: #ab47bc;'>Precio estimado: €{prediccion[0]:.2f}</h3>
        <h4 style='text-align: center; color: #7B7D7D;'>Rango de precio estimado para su Airbnb: €{intervalo_inferior:.2f} - €{intervalo_superior:.2f}</h4>
        <h4 style='text-align: center; color: #7B7D7D;'>Precisión del modelo (R²): {r2:.2f}</h4>
        <p style='text-align: center; color: #7B7D7D; font-size: 14px;'>Un R² de {r2:.2f} indica el nivel de ajuste del modelo a los datos, donde 1 representa un ajuste perfecto.</p>
    </div>
    """, unsafe_allow_html=True)
        
# Aplicación principal
def main():

    
    st.sidebar.title(" 🗺️ Menú de Navegación")  
    page = st.sidebar.selectbox("Selecciona una sección", ("Inicio","Dashboard", "Análisis Exploratorio","Análisis de Reseñas", "Modelo de Predicción"))
    st.sidebar.title("🏙️ Selecciona una ciudad")
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades)

     
    st.sidebar.markdown("### 👥 Equipo")
    
    st.sidebar.markdown(
        '<div class="team-member"><a href="https://www.linkedin.com/in/ignacio-rodriguez-galicia" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" class="linkedin-icon"><span class="member-name">Ignacio Rodríguez Galicia</span></a></div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        '<div class="team-member"><a href="https://www.linkedin.com/in/steven-hurtado-figueroa-41120974?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" class="linkedin-icon"><span class="member-name">Steven Hurtado Figueroa</span></a></div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        '<div class="team-member"><a href="https://www.linkedin.com/in/israel-mart%C3%ADnez-b5742a138?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" class="linkedin-icon"><span class="member-name">Israel Martínez</span></a></div>',
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown(
        '<div class="team-member"><a href="https://www.linkedin.com/in/silvana-ruiz-medina-922397238" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" class="linkedin-icon"><span class="member-name">Silvana Ruiz Medina</span></a></div>',
        unsafe_allow_html=True
    )

# Llamar a cada seccion
    if page == "Inicio":
        inicio()
        
    elif page == "Dashboard" :
        dashboard(df_limpio,ciudad_seleccionada)

    elif page== "Análisis Exploratorio":
        analis_exploratorio(ciudad_seleccionada)

    elif page == "Análisis de Reseñas":
        analisis_resenas(ciudad_seleccionada)
  
    elif page == "Modelo de Predicción":
        modelo_prediccion(ciudad_seleccionada)


if __name__ == "__main__":
    main()
