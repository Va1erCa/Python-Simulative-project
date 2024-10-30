# Module for API-interaction

from datetime import datetime
from dataclasses import dataclass

import config

Celsius = float
start = datetime
end = datetime

@dataclass(slots=True, frozen=True)
class Chunk :
    temperature: Celsius
    weather_type: str
    sunrise: start
    sunset: end
