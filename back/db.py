import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user=os.getenv('DB_USUARIO'),
        password=os.getenv('DB_CONTRASENIA'),
        database=os.getenv('DB_NOMBRE'),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection