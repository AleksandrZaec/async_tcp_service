import asyncio
import logging
from datetime import datetime

from db import init_db, save_request
from config import HOST, PORT

logger = logging.getLogger(__name__)


async def handle_client(reader, writer, conn):
    """
    Функция обрабатывает подключение клиента: принимает данные, сохраняет их в БД и отправляет обратно клиенту.
    """
    addr = writer.get_extra_info('peername')
    logger.info(f'Соединение с {addr} установлено')

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_request(conn, timestamp, message)

            logger.info(f'Получено сообщение: {message} от {addr}')
            writer.write(data)
            await writer.drain()

    except Exception as e:
        logger.error(f'Ошибка при обработке сообщения: {e}')
    finally:
        logger.info(f'Соединение с {addr} закрыто')
        writer.close()
        await writer.wait_closed()


async def start_server(conn):
    """
    Функция запускает сервер, который принимает подключения клиентов и обрабатывает их запросы.
    """
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, conn), HOST, PORT)
    addr = server.sockets[0].getsockname()
    logger.info(f'Сервер запущен на {addr}')

    async with server:
        await server.serve_forever()

