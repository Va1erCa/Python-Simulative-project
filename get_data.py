"""
The module for API-interaction.
"""

from datetime import datetime
from dataclasses import dataclass
import requests, json, logging

# App's modules
import config
from config import CURR_LANG

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
             end_time: datetime | None = None) -> tuple[list[Row], int, int] :

    # Initializing request parameters
    params = {'client': config.REQ_CLIENT,
              'client_key': config.REQ_CLIENT_KEY,
              'start': start_time if start_time else config.REQ_START_TIME,
              'end': end_time if end_time else config.REQ_END_TIME
              }
    res = []
    # executing the request
    try :
        r = requests.get(config.API_URL, params=params)
        r.raise_for_status()    # raise exception if status of request aren't the "ok"
        corrupt_read = 0
        for i, line in enumerate(r.json(), 1) :

            if line['lti_user_id'] is not None:
                res.append(Row(lti_user_id = line.get('lti_user_id', None),
                               passback_params = eval(line.get('passback_params', '{}')),
                               is_correct = line.get('is_correct', None),
                               attempt_type = line.get('attempt_type', None),
                               created_at = line.get('created_at', None)
                               ))

                logger.info(f'{config.LOG_IT_WAS_READ[CURR_LANG][0]}{i}'
                            f'{config.LOG_IT_WAS_READ[CURR_LANG][1]}{res[-1]}')

            else :
                logger.error(f'{config.LOG_ERROR_READ[CURR_LANG][0]}{i}'
                            f'{config.LOG_ERROR_READ[CURR_LANG][1]}')
                corrupt_read += 1

    # work with exceptions
    except requests.HTTPError as e :
        if logger :
            logger.error(f'HTTP Error: {e}')
        else:
            print(f'HTTP Error: {e}')

    except requests.RequestException as e :
        if logger:
            logger.error(f'Request Error: {e}')
        else:
            print(f'Request Error: {e}')

    return res, len(r.json()), corrupt_read


if __name__ == '__main__' :
    print(get_rows())