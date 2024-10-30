# Module for configurations

__doc__ = '''
Модуль конфигурации.
Хранение закрытой информации в .env фале переменных среды окружения.
Содержимое файла .env для корректной работы приложения - закрытые 
параметры API-запроса:
    client=<Имя клиента>
    client_key=<Ключ клиента>[
'''

import environ

# Флаг точного/приблизительного применения координат (False/True)
USE_ROUNDED_COORDS = False

# Координаты по-умолчанию (Заводской)
LATITUDE = 48.403121
LONGITUDE = 40.280044

# Координаты по-умолчанию (Ростов-на-Дону)
# LATITUDE = 47.229060
# LONGITUDE = 39.719080

# чтение секретного api-ключа из файла перенменных среды окружения
env: environ.Env = environ.Env()
environ.Env.read_env()
OPENWEATHER_API: str = env('openweather_api', str)

# Шаблоны для доступа к API сервиса OpenWeather
OPENWEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat={latitude}&lon={longitude}&"
        "appid=" + OPENWEATHER_API + "&lang=ru&"
                                     "units=metric"
)

if __name__ == '__main__' :
    # демо учебных переменных
    ENV_EXAMPLE_LIST = env('env_example_list', list)
    EMV_EXAMPLE_DICT = env('env_example_dict', dict)
    print('Пример работы c переменными среды с помощью библиотеки django_environ:')
    print(f'Итоговый запрос к сервису погоды: {OPENWEATHER_URL}')
    print(f'Переменная среды - список: {ENV_EXAMPLE_LIST}')
    print(f'Переменная среды - словарь: {EMV_EXAMPLE_DICT}')
