import psycopg2
from psycopg2 import sql

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def init_db():
    """
     Функция устанавливает соединение с базой данных PostgreSQL и создает таблицу, если она не существует
    """
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            message TEXT
        )
    ''')
    conn.commit()
    return conn, cursor


def save_request(cursor, timestamp, message):
    """
     Функция сохраняет новый запрос в таблице requests.
    """
    query = sql.SQL("INSERT INTO requests (timestamp, message) VALUES (%s, %s)")
    cursor.execute(query, (timestamp, message))
    cursor.connection.commit()
