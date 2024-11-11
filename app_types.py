'''
A module for common application types
'''

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Row :
    lti_user_id: str
    passback_params: dict
    is_correct: int
    attempt_type: str
    created_at: datetime

@dataclass()
class Line :
    user_id: str
    created_at: datetime
    oauth_consumer_key: str
    lis_result_sourcedid: str
    lis_outcome_service_url: str
    is_correct: bool
    attempt_type: str
