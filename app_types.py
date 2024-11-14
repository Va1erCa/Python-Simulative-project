'''
A module for common application types
'''

import psycopg2
from psycopg2 import extensions
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple
from enum import Enum


import config
from exceptions import ErrorMoreThanOneInstance

# Types
Type_connection = psycopg2.extensions.connection


# Language support
class Language(Enum) :
    RUSSIAN = 0
    ENGLISH = 1


@dataclass(slots=True, frozen=True)
class Row :
    lti_user_id: str
    passback_params: dict
    is_correct: bool
    attempt_type: str
    created_at: datetime


# Setting the structure by the class
# @dataclass()
# class Line :
#     user_id: str
#     created_at: datetime
#     oauth_consumer_key: str
#     lis_result_sourcedid: str
#     lis_outcome_service_url: str
#     is_correct: bool
#     attempt_type: str


# Creating a structure by inheriting from a named typed tuple
# ATTENTION, AN ORDER THE FIELDS IN NAMED TUPLE MAST BE EQUALS WITH AN ORDER FIELDS IN SQL-QUERY FOR INSERT DATA
class Line(NamedTuple) :
    user_id: str
    created_at: datetime
    oauth_consumer_key: str
    lis_result_sourcedid: str
    lis_outcome_service_url: str
    is_correct: bool
    attempt_type: str


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

