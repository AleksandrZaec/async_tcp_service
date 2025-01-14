import os

HOST = 'localhost'
PORT = 8000

DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')

NUM_CLIENTS = 10
MESSAGE_INTERVAL = (5, 10)
CONNECTION_TIMEOUT = 10