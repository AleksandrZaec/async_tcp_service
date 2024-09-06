import asyncio
import random
import logging

from config import HOST, PORT, NUM_CLIENTS, MESSAGE_INTERVAL, CONNECTION_TIMEOUT

logger = logging.getLogger(__name__)


async def tcp_client(client_id):
    """
    Функция запускает TCP-клиента, который подключается к серверу, отправляет сообщения и получает ответы.
    """
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(HOST, PORT), timeout=CONNECTION_TIMEOUT)
    except asyncio.TimeoutError:
        logger.error(f'Клиент {client_id}: не удалось подключиться к серверу, время ожидания истекло')
        return
    except Exception as e:
        logger.error(f'Клиент {client_id}: ошибка при подключении к серверу: {e}')
        return

    for i in range(5):
        await asyncio.sleep(random.randint(*MESSAGE_INTERVAL))
        message = f'Клиент {client_id} сообщение {i + 1}'
        logger.info(f'Отправка: {message}')
        writer.write(message.encode())
        await writer.drain()

        try:
            data = await asyncio.wait_for(reader.read(100), timeout=CONNECTION_TIMEOUT)
            logger.info(f'Получен эхо-ответ: {data.decode()}')
        except asyncio.TimeoutError:
            logger.error(f'Клиент {client_id}: не получил ответ от сервера, время ожидания истекло')
        except Exception as e:
            logger.error(f'Клиент {client_id}: ошибка при получении данных: {e}')

    logger.info(f'Клиент {client_id} закрывает соединение')
    writer.close()
    await writer.wait_closed()


async def start_clients():
    """
    Функция запускает заданное количество клиентов параллельно.
    """

    await asyncio.sleep(5)
    tasks = [tcp_client(i) for i in range(1, NUM_CLIENTS + 1)]
    await asyncio.gather(*tasks)
