import asyncio
import logging

from db import init_db
from server import start_server
from client import start_clients

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


async def main():
    """
    Основная асинхронная функция, которая запускает сервер, клиентов и управляет соединением с базой данных.
    """
    conn, cursor = init_db()
    server_task = asyncio.create_task(start_server(cursor))
    await asyncio.sleep(5)
    await start_clients()
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        logging.info('Сервер остановлен')


if __name__ == '__main__':
    asyncio.run(main())
