'''
A module for common application types
'''

from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple


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