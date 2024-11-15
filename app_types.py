'''
A module for common application types
'''

import psycopg2
from psycopg2 import extensions
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple
from enum import Enum

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


# The structure to use in the Google Sheets report
class Report(NamedTuple) :
    proccess_date: int
    total_unique_users: int
    total_runs: int
    total_submits: int
    total_success_submits: int
    ratio_success_submits: float
    avg_number_submits_per_user: float
    avg_number_success_submits_per_user: float
    empty_row1: str
    report_date: int
