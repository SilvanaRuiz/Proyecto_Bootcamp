# Proyecto de Análisis de Datos de Airbnb

Este proyecto consiste en el desarrollo de una aplicación web interactiva para estudiar el mercado de listados de Airbnb en varias ciudades, permitiendo un análisis de datos profundo mediante visualizaciones y herramientas. La aplicación se construye en **Streamlit** e incorpora técnicas de Machine Learning y procesamiento de lenguaje natural (NLP) para ofrecer insights detallados tanto de las propiedades como de sus reseñas.

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
- Utilizar técnicas de procesamiento de lenguaje natural para analizar las reseñas de los listados, generando insights específicos sobre las propiedades.

## Características Principales

- **Dashboard interactivo**: Un panel para explorar datos de listados de Airbnb con filtros y paginación.
- **Mapa interactivo**: Un mapa de la ciudad seleccionada donde se puede visualizar una variable de interés.
- **Visualizaciones**: Múltiples gráficos sobre la distribución de precios, calificaciones, tipos de anfitrión, y otras variables relevantes.
- **Análisis de Reseñas con NLP**: Análisis específico de reseñas utilizando técnicas de procesamiento de lenguaje natural.
- **Herramienta de IA**: Permite analizar enlaces de listados de Airbnb, almacenando los resultados y mostrando visualizaciones clave.
- **ETL Automático**: Un proceso ETL que actualiza la base de datos con nueva información cuando es necesario.

## Estructura del Proyecto

El proyecto sigue una estructura modular para una fácil navegación y mantenimiento. 

├── csv_files/ │ ── Stremlit_26.py # Código principal de la aplicación Streamlit ├── models/ # Modelos de ML y NLP ├── notebooks/ # Jupyter notebooks para experimentación y pruebas ├── requirimientos.txt # Dependencias └── README.md 

# Documentación del proyecto


### Descripción de Archivos
- **csv_files/**: Contiene los datos limpios de Airbnb de diferentes ciudades.
- **.py**: Archivo principal que maneja la interfaz de usuario y las visualizaciones en Streamlit.
- **models/**: Incluye los modelos de Machine Learning y NLP entrenados.
- **notebooks/**: Notebooks para el análisis y experimentación de datos.

---

## Descripción de la Aplicación

La aplicación incluye varias vistas que permiten interactuar con los datos y visualizaciones de Airbnb:

### 1. Vista de Dashboard
   - **Navegación y Filtrado**: Permite explorar listados mediante filtros y paginación.
   - **Mapa Interactivo**: Muestra las ubicaciones de las propiedades en la ciudad seleccionada, con variables de interés visibles.
   - **Visualizaciones**: Incluye gráficos de distribución de calificación, precios, tipos de anfitrión, y más.
   
### 2. Vista de Análisis de Reseñas
   - **Análisis NLP**: Utiliza técnicas de procesamiento de lenguaje natural para extraer insights de las reseñas.
   - **Visualizaciones Específicas**: Al menos cinco gráficos dedicados exclusivamente al análisis de reseñas.

### 3. Herramienta de IA para Listados
   - **Análisis de Listados**: Permite ingresar un enlace de Airbnb y obtener insights específicos.
   - **Almacenamiento de Resultados**: Los análisis se almacenan en un dataframe que se puede expandir.
   - **Métrica de Calidad**: Calcula una métrica que clasifica la calidad del listado.

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
- pandas- 
- plotly
- seaborn
- matplotlib
- scikit-learn
- nltk


## Ejecutar la Aplicación

git clone <url>
cd <nombre>

### Instala las dependencias:

pip install -r requirementos.txt

#### Ejecuta la aplicación con Streamlit:

python -m streamlit run streamlit_26.py
