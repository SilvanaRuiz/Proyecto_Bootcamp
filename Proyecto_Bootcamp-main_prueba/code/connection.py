import pymysql
import os

def get_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )
    except Exception as e:
        print("Error de conexión a la base de datos:", e)
        return None

