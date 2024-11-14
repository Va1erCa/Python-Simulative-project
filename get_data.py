"""
The module for API-interaction.
"""

from datetime import datetime, date
import requests, json, logging

# App's modules
import config
from config import CURR_LANG
from app_types import Row
from logger import Mylogger


def get_rows(logger: Mylogger, start_time: datetime, end_time: datetime) -> list[Row] :
    '''
    Requesting/receiving data from a network resource
    :param logger: A logger for recording history
    :param start_time: Start - timestamp
    :param end_time: End - timestamp
    :return: a list of all success readed  Row-class instances
    '''

    # The starting mark in the log for api-working with selected time interval
    logger.msg_api_start_work(start_time, end_time)

    # Initializing request parameters
    params = {'client' : config.REQ_CLIENT,
              'client_key' : config.REQ_CLIENT_KEY,
              'start' : start_time,
              'end' : end_time}
    res = []
    total_readed = 0
    corrupt_readed = 0
    # executing the request
    try :
        r = requests.get(config.API_URL, params=params)
        r.raise_for_status()  # raise exception if status of request aren't the "ok"
        total_readed = len(r.json())

        for i, line in enumerate(r.json(), 1) :
            if line['lti_user_id'] is not None :
                res.append(Row(lti_user_id=line.get('lti_user_id', None),
                               passback_params=eval(line.get('passback_params', '{}')),
                               is_correct=line.get('is_correct', None),
                               attempt_type=line.get('attempt_type', None),
                               created_at=line.get('created_at', None)
                               ))

                if config.LOG_EVERY_INCOMING_LINE :
                    logger.msg_api_row_was_read(i, res[-1])  # if set flag, all rows logging

            else :
                logger.msg_api_row_was_error_read(i)  # error logging
                corrupt_readed += 1

    # work with exceptions
    except requests.HTTPError as e :
        logger.msg(logging.ERROR, f'HTTP Error: {e}')

    except requests.RequestException as e :
        logger.msg(logging.ERROR, f'Request Error: {e}')

    # The ending mark in the log for api-working with date
    logger.msg_api_end_work(total_readed, corrupt_readed)

    return res


if __name__ == '__main__' :
    logger = Mylogger(date.fromisoformat('2024-10-01'))
    start_time = datetime.fromisoformat('2024-10-01 00:00:00.000000')
    end_time = datetime.fromisoformat('2024-10-01 00:59:59.999999')
    print(get_rows(logger, start_time, end_time))
