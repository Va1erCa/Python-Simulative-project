# Main module.

from datetime import datetime

from get_data import get_rows
from logger import get_my_logger


def get_process_date() -> tuple[datetime | None, datetime | None] :
    '''
    Запрос у пользователя даты за которую будет произведена обработка
    :return: кортеж таймстемпов начала введенной даты и ее конца
    '''
    while True:
        start_time, end_time = None, None
        str_date = input('Введите дату извлечения данных в формате: <YYYY-mm-dd> или <exit> для выхода: ')
        if str_date.lower() == 'exit': break
        try:
            start_time = datetime.fromisoformat(str_date + ' 00:00:00.000000')
            end_time = datetime.fromisoformat(str_date + ' 23:59:59.999999')
            break
        except ValueError:
            print('Ошибка ввода даты, попробуйте еще раз...\n')
            continue

    return start_time, end_time


def main():
    # запрашиваем у пользователя дату, которую будем обрабатывать
    start_time, end_time = get_process_date()
    if start_time :
        # инициализируем наш логгер
        my_logger, _ = get_my_logger()
        my_logger.info('скачивание данных началось')
        # Получаем строки
        # rows = get_rows(my_logger, start_time=start_time, end_time=end_time)
        my_logger.info('скачивание данных завершено')
        # Вносим информацию в базу данных
        my_logger.info('загрузка данных в базу началась')
        # put_in_base(my_logger, rows)
        my_logger.info('загрузка данных в базу завершена')


if __name__ == '__main__':
    main()