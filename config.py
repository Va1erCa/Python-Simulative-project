# Module for configurations

__doc__ = '''
Модуль конфигурации.
Хранение закрытой информации в .env фале переменных среды окружения.
Содержимое файла .env для корректной работы приложения - закрытые 
параметры API-запроса:
    client=<Имя клиента>
    client_key=<Ключ клиента>[
'''

from datetime import datetime
import environ

# чтение закрытых данных из файла перенменных среды окружения
env = environ.Env()
environ.Env.read_env()

# endpoint сервиса статистики он-лайн университета
API_URL = "https://b2b.itresume.ru/api/statistics"

# параметры обращения к api
REQ_CLIENT = env('client', str)
REQ_CLIENT_KEY = env('client_key', str)
REQ_START_TIME = datetime.fromisoformat('2023-04-01 00:00:00.000000')
REQ_END_TIME = datetime.fromisoformat('2023-04-01 00:01:59.999999')


if __name__ == '__main__' :
    print(f"client: {env('client', str)}, client_key: {'#'*len(env('client_key', str))}")

