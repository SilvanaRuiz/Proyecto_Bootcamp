# Proyecto de Análisis de Datos de Airbnb

Este proyecto se centra en crear una aplicación web interactiva para analizar el mercado de listados de Airbnb en diversas ciudades. La aplicación, desarrollada en **Streamlit**, integra técnicas de Machine Learning y procesamiento de lenguaje natural (NLP) para proporcionar insights detallados sobre las propiedades y sus reseñas.

## Tabla de Contenidos
- [Objetivo del Proyecto](#objetivo-del-proyecto)
- [Características Principales](#características-principales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Descripción de la Aplicación](#descripción-de-la-aplicación)
- [Objetivos Específicos](#objetivos-específicos)
- [Requerimientos](#requerimientos)
- [Ejecutar la Aplicación](#ejecutar-la-aplicación)
- [Contribuciones](#contribuciones)

---

## Objetivo del Proyecto

El propósito de este proyecto es desarrollar una aplicación que permita:
- Analizar el mercado de Airbnb de ciudades seleccionadas.
- Facilitar la exploración de datos y la toma de decisiones mediante visualizaciones interactivas y un modelo de predicción de propiedades.
- Aplicar técnicas de procesamiento de lenguaje natural (NLP) para analizar las reseñas de los alojamientos y compararlas con la calificación otorgada en Airbnb.

## Características Principales

- **Dashboard interactivo**: Un panel para explorar datos de listados de Airbnb con filtros y paginación.
- **Visualizaciones**: Múltiples gráficos sobre la distribución de precios, calificaciones, tipos de anfitrión, y otras variables relevantes.
- **Análisis de Reseñas con NLP**: Análisis específico de reseñas utilizando técnicas de procesamiento de lenguaje natural.
- **Modelo de predicción**: Permite analizar enlaces de listados de Airbnb, almacenando los resultados y mostrando visualizaciones clave.

## Estructura del Proyecto

El proyecto sigue una estructura modular para una fácil navegación y mantenimiento. 

├── objetos/                # Contiene archivos auxiliares y modelos preentrenados
│   ├── Airbnb.csv.zip      # Archivo comprimido con los datos de Airbnb en formato CSV
│   ├── bathroom_columns.pkl, city_columns.pkl, columnas_X.pkl  # Archivos de columnas para los modelos
│   ├── encoder_bathroom.pkl, encoder_city.pkl  # Encoders necesarios para el procesamiento de datos
│   ├── modelo_c0.pkl, modelo_c1.pkl, modelo_c2.pkl, modelo_clasificacion.pkl  # Modelos de ML en formato .pkl
│   ├── percentiles_modelo0.pkl, percentiles_modelo1.pkl, percentiles_modelo2.pkl  # Archivos de percentiles para los modelos
│   └── resultados_nlp.csv   # Archivo CSV con resultados de procesamiento NLP
│
├── code/                   # Contiene scripts y notebooks de desarrollo
│   ├── __init__.py         # Inicializador de módulo para la carpeta code
│   ├── base_datos.py       # Script de gestión de base de datos
│   ├── connection.py       # Script para la conexión con la base de datos
│   ├── creacion_reseñas.py # Generación y procesamiento de reseñas
│   ├── limpieza.py         # Limpieza y preprocesamiento de datos
│   ├── scraping.py         # Script de scraping de datos
│   ├── modelo precio.ipynb # Jupyter notebook para modelado de precios
│   └── modelo_junto.ipynb  # Jupyter notebook de modelos combinados
│
├── Streamlit_26.py         # Código principal de la aplicación en Streamlit
│
├── requirements.txt        # Lista de dependencias del proyecto
│
└── README.md               # Documentación general del proyecto

---

## Descripción de la Aplicación

La aplicación incluye varias vistas que permiten interactuar con los datos y visualizaciones de Airbnb:

### 1. Vista de Dashboard
   - **Navegación y Filtrado**: Permite explorar listados mediante filtros y paginación.
   - **Visualización de Datos Clave**: Estadísticas generales como total de alojamientos, rating promedio y precio promedio.
   - **Actualización de Datos**: Explicación del proceso de scraping con opción de descarga para obtener datos actualizados.
     
### 2. Vista Análisis Exploratorio
   - Esta sección permite visualizar datos clave de los listados de Airbnb en la ciudad seleccionada mediante diversos gráficos interactivos.
   - **Distribución de Calificación y Precio**: Histogramas que muestran la dispersión de calificaciones y precios de los alojamientos.
   - **Precio por Tipo de Anfitrión**: Gráficos que destacan la variabilidad de precios según el tipo de anfitrión.
   - **Relaciones entre Variables**: Visualizaciones de la relación entre precio y calificación, y entre experiencia del anfitrión y precio.
   - **Mapa de Calo**r: Correlación entre variables para identificar patrones en los datos.

### 3. Vista de Análisis de Reseñas
   - **Análisis NLP**: Utiliza técnicas de procesamiento de lenguaje natural para extraer insights de las reseñas.

### 4. Vista del Modelo de Predicción
   - **Explicación Metodológica**: Documentación del desarrollo y las métricas de rendimiento del modelo.
   - **Visualización de Resultados**: Gráficos para ilustrar el desempeño del modelo.

---

## Objetivos Específicos

Este proyecto aborda objetivos técnicos, analíticos, y de desarrollo en equipo:

### Tecnológicos y Analíticos
- Desarrollar un **frontend interactivo** en Streamlit que permita interactuar con los datos y el modelo.
- Crear un **dashboard intuitivo y amigable** que facilite la comprensión de los datos a usuarios no técnicos.
- Diseñar un **proceso ETL** independiente que mantenga los datos actualizados para la aplicación y otros sistemas.
- Mantener un **control de calidad de datos** riguroso desde la recopilación hasta la evaluación del modelo.
- Justificar las **decisiones de limpieza y preprocesamiento** de los datos para cumplir con los requisitos del proyecto.
- Utilizar **buenas prácticas de desarrollo** y un sistema de control de versiones.

### Habilidades Complementarias
- Fomentar la **colaboración en equipo** para resolver los desafíos del proyecto.
- Mejorar las **habilidades de comunicación efectiva** tanto en el equipo como con stakeholders.
- Implementar **metodologías ágiles** y participar en ceremonias como reuniones de Scrum y revisiones de progreso.
- Proponer **soluciones innovadoras** que beneficien a los usuarios y mejoren la experiencia de uso de la aplicación.

---

## Requerimientos

### Dependencias Principales
- streamlit
- pandas 
- plotly
- seaborn
- matplotlib
- scikit-learn
- nltk
- selenium

### Instala las dependencias:

pip install -r requirementos.txt

#### Ejecuta la aplicación con Streamlit:

python -m streamlit run Streamlit_26.py

### Acceder a la aplicación
https://proyectobootcampairbnb.streamlit.app/
Para evitar descargas, puedes acceder directamente a la aplicación copiando este enlace o buscando en Streamlit: **Análisis de Mercado de Airbn**.
