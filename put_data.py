"""
The module for PostgreSQL-server interaction.
"""

import psycopg2
from psycopg2 import extensions
import logging

# App's modules
import config
from config import CURR_LANG
from exceptions import ErrorMoreThanOneInstance
from app_types import Row, Line

# Types
Type_connection = psycopg2.extensions.connection

# Parameters for work database table
#
# Query for creating the main table in the database
DB_MAIN_TABLE_CREATE_QUERY = (f'CREATE TABLE {config.DB_MAIN_TABLE_NAME} '
                              f'(user_id VARCHAR, '
                              f'created_at TIMESTAMP, '
                              f'oauth_consumer_key VARCHAR, '
                              f'lis_result_sourcedid VARCHAR, '
                              f'lis_outcome_service_url VARCHAR, '
                              f'is_correct BOOLEAN, '
                              f'attempt_type VARCHAR);'
                              )
# Query to find the main table in the database
DB_MAIN_TABLE_SEARCH_QUERY = (f'SELECT table_name FROM information_schema.tables '
                              f'WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\' '
                              f'AND table_name = \'{config.DB_MAIN_TABLE_NAME}\''
                              )
# Query to clear the main table in the database
DB_MAIN_TABLE_CLEAR_QUERY = f'DELETE FROM {config.DB_MAIN_TABLE_NAME}'
# Query to insert one record into the main table in the database
DB_MAIN_TABLE_INSERT_DATA_QUERY = (f'INSERT INTO {config.DB_MAIN_TABLE_NAME} ('
                                   f'user_id, created_at, oauth_consumer_key, lis_result_sourcedid, '
                                   f'lis_outcome_service_url, is_correct, attempt_type) '
                                   f'VALUES (%s, %s, %s, %s, %s, %s, %s);'
                                   )
# Query to demonstrate all data in the main table in the database
DB_MAIN_TABLE_TEST_SELECT_QUERY = f'select * from {config.DB_MAIN_TABLE_NAME}'


class DatabaseConnection :
    __instance = None  # A variable for saving an instance of the DatabaseConnection class

    @staticmethod  # An interface method (static) for accessing an instance of the DatabaseConnection class
    def get_instance(**kwargs: object) -> object :
        if not DatabaseConnection.__instance :
            DatabaseConnection(**kwargs)
        return DatabaseConnection.__instance

    def __init__(self, **params) -> None :
        if DatabaseConnection.__instance :
            raise ErrorMoreThanOneInstance
        else :
            # Processing parameters
            pr = config.SERVER_CONNECTION_PARAMS.copy()  # Copying dictionary with default parameters
            pr.update(params)  # Update if the parameters have been passed to the constructor
            pr_autocommit = pr.pop('autocommit')  # The 'autocommit' parameter will be used outside the 'pr'-dict

            # Creating an instance of the DatabaseConnection class
            self.connection = psycopg2.connect(**pr)
            self.connection.autocommit = pr_autocommit  # Set up 'autocommit'

            # assign a single instance of the class to a class variable
            DatabaseConnection.__instance = self

    def get_connection(self) -> Type_connection :
        return self.connection

    def close(self) -> None :
        self.connection.close()


def init_data_base(logger: logging.Logger | None = None) -> DatabaseConnection | None :
    '''

    :param logger:
    :return:
    '''

    try :
        database_connection = DatabaseConnection()
        connection = database_connection.get_connection()
        with connection :
            with connection.cursor() as cursor :
                # Searching main table in the database
                cursor.execute(DB_MAIN_TABLE_SEARCH_QUERY)
                if len(cursor.fetchall()) == 0 :
                    # If the main table is not found, creating it
                    cursor.execute(DB_MAIN_TABLE_CREATE_QUERY)
                elif config.DB_MAIN_TABLE_OPEN_RESET :
                    # Clearing the main table if there is one and the flag is set
                    cursor.execute(DB_MAIN_TABLE_CLEAR_QUERY)

    except psycopg2.Error as err :
        database_connection = None
        if logger :
            logger.error(f'Database init error: {err}')
        else :
            print(f'Database init error: {err}')

    return database_connection


def insert_line(line: int, connection: Type_connection, row: Row, logger: logging.Logger | None = None) -> bool :
    clean_data = True
    with connection :
        cursor = connection.cursor()

        new_record = Line(user_id = row.lti_user_id,
                          created_at = row.created_at,
                          oauth_consumer_key = row.passback_params.get('oauth_consumer_key', None),
                          lis_result_sourcedid = row.passback_params.get('lis_result_sourcedid', None),
                          lis_outcome_service_url = row.passback_params.get('lis_outcome_service_url', None),
                          is_correct = None if row.is_correct is None else bool(row.is_correct),
                          attempt_type = row.attempt_type)

        # Data quality control
        err = f'{config.LOG_OMISSION_IN_THE_DATA[CURR_LANG]}<oauth_consumer_key>' if new_record.oauth_consumer_key is None else ''
        err += f'{config.LOG_OMISSION_IN_THE_DATA[CURR_LANG]}<lis_result_sourcedid>' if new_record.lis_result_sourcedid is None else ''
        err += f'{config.LOG_OMISSION_IN_THE_DATA[CURR_LANG]}<lis_outcome_service_url>' if new_record.lis_outcome_service_url is None else ''
        err += f'{config.LOG_INCORRECT_COMBINATION_OF_PARAMETERS[CURR_LANG]} <is_correct>/<attempt_type>' if (
                            (new_record.is_correct is None and new_record.attempt_type == 'submit') or
                            (new_record.is_correct is not None and new_record.attempt_type == 'run')) else ''
        if len(err) > 0 :
            # If there are errors, we register them
            clean_data = False
            if logger is not None:
                logger.error(f'{config.LOG_ERROR_IN_THE_DATA[CURR_LANG][0]}{line}'
                             f'{config.LOG_ERROR_IN_THE_DATA[CURR_LANG][1]}{err}')
            else:
                print(f'{config.LOG_ERROR_IN_THE_DATA[CURR_LANG][0]}{line}'
                      f'{config.LOG_ERROR_IN_THE_DATA[CURR_LANG][1]}{err}')

        # Adding data to the main table
        cursor.execute(DB_MAIN_TABLE_INSERT_DATA_QUERY, (new_record.user_id,
                                                         new_record.created_at,
                                                         new_record.oauth_consumer_key,
                                                         new_record.lis_result_sourcedid,
                                                         new_record.lis_outcome_service_url,
                                                         new_record.is_correct,
                                                         new_record.attempt_type)
                       )
        # connection.commit()
        cursor.close()
    return clean_data


def put_in_base(rows: list[Row], logger: logging.Logger | None = None) -> tuple[int, int]:
    '''

    :param rows:
    :param logger:
    :return:
    '''

    total_writed = 0
    defect_writed = 0

    db_connector = init_data_base()
    if db_connector is not None :
        my_connection = db_connector.get_connection()

        for i, row in enumerate(rows, 1):
            if not insert_line(i, my_connection, row, logger) :
                defect_writed += 1
            total_writed += 1

        db_connector.close()

    return total_writed, defect_writed


if __name__ == '__main__' :
    db_connector = init_data_base()
    my_connection = db_connector.get_connection()
    with my_connection :
        with my_connection.cursor() as cursor :
            cursor.execute(DB_MAIN_TABLE_TEST_SELECT_QUERY)
            res = cursor.fetchall()
            print(res)
    db_connector.close()
