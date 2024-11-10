"""
The module for PostgreSQL-server interaction.
"""

import psycopg2
from psycopg2 import extensions
import logging

# App's modules
import config
from exceptions import ErrorMoreThanOneInstance

# Types
Type_connection = psycopg2.extensions.connection


class DatabaseConnection:

    __instance = None   # A variable for saving an instance of the DatabaseConnection class

    @ staticmethod      # An interface method (static) for accessing an instance of the DatabaseConnection class
    def get_instance(**kwargs: object) -> object:
        if not DatabaseConnection.__instance:
            DatabaseConnection(**kwargs)
        return DatabaseConnection.__instance

    def __init__(self, **params) -> None:
        if DatabaseConnection.__instance:
            raise ErrorMoreThanOneInstance
        else:
            # Processing parameters
            pr = config.SERVER_CONNECTION_PARAMS.copy()     # Copying dictionary with default parameters
            pr.update(params)           # Update if the parameters have been passed to the constructor
            pr_autocommit = pr.pop('autocommit')        # The 'autocommit' parameter will be used outside the 'pr'-dict

            # Creating an instance of the DatabaseConnection class
            self.connection = psycopg2.connect(**pr)
            self.connection.autocommit = pr_autocommit  # Set up  'autocommit'

            # assign a single instance of the class to a class variable
            DatabaseConnection.__instance = self

    def get_connection(self) -> Type_connection :
        return self.connection

    def close(self) -> None:
        self.connection.close()


def init_data_base(logger: logging.Logger | None = None) -> DatabaseConnection | None :
    try:
        database_connection = DatabaseConnection()
        # try:
        # database_connection = DatabaseConnection.get_instance(port=5432)
    except psycopg2.Error as err:
        database_connection = None
        if logger :
            logger.error(f'Database init error: {err}')
        else:
            print(f'Database init error: {err}')
    return database_connection


if __name__ == '__main__' :
    db_connector = init_data_base()
    my_connection = db_connector.get_connection()
    with my_connection:
        with my_connection.cursor() as curs :
            curs.execute('select * from test_ddl')
            res = curs.fetchall()
            print(res)
    db_connector.close()
