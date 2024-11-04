"""
The module for API-interaction.
"""

from datetime import datetime
from dataclasses import dataclass
import requests, json, logging


import config

start = datetime
end = datetime


@dataclass(slots=True, frozen=True)
class Row :
    lti_user_id: str
    passback_params: dict
    is_correct: bool
    attempt_type: str
    created_at: datetime


def get_rows(logger: logging.Logger | None = None,
             start_time: datetime | None = None,
             end_time: datetime | None = None) -> list[Row] :
    # инициализация параметров запроса
    params = {'client': config.REQ_CLIENT,
              'client_key': config.REQ_CLIENT_KEY,
              'start': start_time if start_time else config.REQ_START_TIME,
              'end': end_time if end_time else config.REQ_END_TIME
              }
    # запрос на получение данных
    try :
        r = requests.get(config.API_URL, params=params)
        r.raise_for_status()    # бросаем ошибку если статус запроса "не Ok"

    # обработка ошибок запроса
    except requests.HTTPError as e :
        if logger :
            logger.error(f'HTTP Error: {e}')
        else:
            print(f'HTTP Error: {e}')
        return []
    except requests.RequestException as e :
        if logger:
            logger.error(f'Request Error: {e}')
        else:
            print(f'Request Error: {e}')
        return []

    return r.json()


if __name__ == '__main__' :
    print(get_rows())