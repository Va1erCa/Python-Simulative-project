"""
The module for Postgres-server interaction.
"""

import psycopg2
from psycopg2 import extensions
from datetime import date
import logging

# App's modules
import config
from app_types import Row, Line
from logger import Mylogger
from exceptions import ErrorMoreThanOneInstance, ErrorInsertingLine


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
DB_MAIN_TABLE_TEST_SELECT_QUERY = f'select * from {config.DB_MAIN_TABLE_NAME} LIMIT 10'


class DatabaseConnection :
    '''
    Singleton class for saving a database connection object
    '''
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


def create_database_connection(logger: Mylogger) -> DatabaseConnection | None :
    db_connection = None
    try :
        db_connection = DatabaseConnection()
    except psycopg2.Error as err:
        logger.msg_creating_database_connection_error(err)

    return db_connection


def init_data_base(logger: Mylogger, db_connection: DatabaseConnection) -> bool :
    '''
    Initialize the database infrastructure and create the main table, if necessary.
    :param logger: A logger for recording history
    :return: DatabaseConnection - object
    '''
    result = True
    try :
        with db_connection.get_connection() as connection:
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
        result = False
        logger.msg_main_table_init_error({err})

    return result


def insert_line(logger: Mylogger, line: int, connection: Type_connection, row: Row) -> bool :
    '''
    Function that inserting one line into main table. It's returning flag of correct data that was processed.
    :param logger: A logger for recording history
    :param line: The number of the current line for logging by the logger
    :param connection: DatabaseConnection - object
    :param row: Input data row
    :return: A flag for the correctness of the data that has been processed.
    '''
    clean_data = True   # A flag for the correctness of the data that has been processed
    try :
        with connection :
            cursor = connection.cursor()

            # Adding data to the main table - Variant1 - with passing arguments using the 'dataclass' structure
            # cursor.execute(DB_MAIN_TABLE_INSERT_DATA_QUERY, new_record.user_id,
            #                                                  new_record.created_at,
            #                                                  new_record.oauth_consumer_key,
            #                                                  new_record.lis_result_sourcedid,
            #                                                  new_record.lis_outcome_service_url,
            #                                                  new_record.is_correct,
            #                                                  new_record.attempt_type)
            #                )

            # Adding data to the main table - Variant2 - with passing arguments using the 'NamedTuple' tuple
            new_record = Line(user_id=row.lti_user_id,
                              created_at=row.created_at,
                              #     This variant is used if an empty string in the 'oauth_consumer_key' field
                              #     should be treated as an error:
                              # oauth_consumer_key=(None if row.passback_params.get('oauth_consumer_key', '') == ''
                              #                     else row.passback_params['oauth_consumer_key']),
                              oauth_consumer_key=row.passback_params.get('oauth_consumer_key', None),
                              lis_result_sourcedid=row.passback_params.get('lis_result_sourcedid', None),
                              lis_outcome_service_url=row.passback_params.get('lis_outcome_service_url', None),
                              is_correct=None if row.is_correct is None else bool(row.is_correct),
                              attempt_type=row.attempt_type)

            # Data quality control
            error = ('#<oauth_consumer_key>' if new_record.oauth_consumer_key is None else '') + (
                     '#<lis_result_sourcedid>' if new_record.lis_result_sourcedid is None else '') + (
                     '#<lis_outcome_service_url>' if new_record.lis_outcome_service_url is None else '') + (
                     '$<is_correct>/<attempt_type>' if ((new_record.is_correct is None
                                                        and new_record.attempt_type == 'submit') or
                                                       (new_record.is_correct is not None
                                                        and new_record.attempt_type == 'run')) else '')
            if len(error) > 0 :
                # If there are errors, we register them
                logger.msg_omission_or_incorrect_data(line, error)
                clean_data = False

            cursor.execute(DB_MAIN_TABLE_INSERT_DATA_QUERY, new_record)

            # connection.commit()
            cursor.close()
    except psycopg2.Error as err:
        logger.msg_error_insert_line(err)
        raise ErrorInsertingLine

    return clean_data


def put_in_base(logger: Mylogger, db_connection: DatabaseConnection, rows: list[Row], ) -> bool :
    '''
    The main function of uploading all read data to the database.
    :param logger: A logger for recording history
    :param rows: A list of Row-class instances
    :return: A tuple of two values:
            the number of all recorded output lines,
            the number of all recorded output lines with incomplete data
    '''

    total_writed = 0
    defect_writed = 0
    result = True
    if init_data_base(logger, db_connection) :
        my_connection = db_connection.get_connection()
        for i, row in enumerate(rows, 1) :
            try :
                if not insert_line(logger, i, my_connection, row) :
                    defect_writed += 1
                total_writed += 1
            except ErrorInsertingLine :
                pass
        # The ending mark in the log about loading data in database
        logger.msg_dbms_end_work(len(rows), total_writed, defect_writed)
    else:
        db_connection.close()
        result = False

    return result


if __name__ == '__main__' :
    logger = Mylogger(date(2024, 10, 1))
    db_connection = create_database_connection(logger)
    if init_data_base(logger, db_connection) :
        my_connection = db_connection.get_connection()
        with my_connection :
            with my_connection.cursor() as cursor :
                cursor.execute(DB_MAIN_TABLE_TEST_SELECT_QUERY)
                result = cursor.fetchall()
                print(result)

    db_connection.close()
