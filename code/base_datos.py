import pandas as pd
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid
from objetos.connection import get_connection  # Importar la función de conexión

# Crear la base declarativa para el ORM de SQLAlchemy
Base = declarative_base()

# Definir la clase Airbnb que mapea a la tabla airbnb_listings_1
class Airbnb(Base):
    __tablename__ = 'airbnb_listings_1'

    unique_id = Column(String(50), primary_key=True, unique=True)  # UUID como clave primaria
    title = Column(String(200))
    city = Column(String(200))
    guest_favorite = Column(String(200))
    rating = Column(Text)
    number_reviews = Column(String(200))
    type_host = Column(String(200))
    hosting_time = Column(String(200))
    price = Column(String(200))
    all_reviews = Column(LONGTEXT)
    complete_data_list = Column(Text)
    url = Column(Text)
    id_url = Column(String(100), unique=True)


def bd(df):
    df = df.where(pd.notnull(df), None)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    df['type_host'] = df['type_host'].apply(lambda x: 'normal' if pd.isna(x) else x)

    def create_schema_and_populate_db(df):
        # Obtener la conexión segura desde connection.py
        connection = get_connection()
        if connection is None:
            print("No se pudo establecer la conexión con la base de datos.")
            return

        # Crear un engine usando la conexión establecida
        engine = create_engine('mysql+pymysql://', creator=lambda: connection)

        # Crear el esquema en la base de datos (si no existe)
        Base.metadata.create_all(engine)

        # Crear una sesión
        Session = sessionmaker(bind=engine)
        session = Session()

        for _, row in df.iterrows():
            unique_id = str(uuid.uuid4())
            try:
                listing = Airbnb(
                    unique_id=unique_id,
                    title=row.get('title', None),
                    city=row.get('city', None),
                    guest_favorite=row.get('guest_favorite', None),
                    rating=row.get('rating', None),
                    type_host=row.get('type_host', None),
                    hosting_time=row.get('hosting_time', None),
                    price=row.get('price', None),
                    number_reviews=row.get('number_reviews', None),
                    all_reviews=row.get('all_reviews', None),
                    complete_data_list=row.get('complete_data_list', None),
                    id_url=row.get('id_url', None),
                    url=row.get('url', None)
                )
                session.merge(listing)
            except Exception as e:
                print(f"Error al insertar los datos: {e}")
                continue

        session.commit()
        session.close()

    create_schema_and_populate_db(df)


def extract_data_from_db():
    # Obtener la conexión segura desde connection.py
    connection = get_connection()
    if connection is None:
        print("No se pudo establecer la conexión con la base de datos.")
        return pd.DataFrame()

    # Crear un engine usando la conexión segura
    engine = create_engine('mysql+pymysql://', creator=lambda: connection)

    # Consulta SQL para seleccionar todos los registros de la tabla
    query = "SELECT * FROM airbnb_listings_1"
    df = pd.read_sql(query, engine)

    return df

