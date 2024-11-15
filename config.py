"""
The module for configuration.
"""

# The storage of private information is organized in the .env file of environment variables.
# The contents of the .env file for the correct operation of the application are closed API request parameters:
#   client=<client's name>
#   client_key=<client's key>


from datetime import datetime, date
import environ
from app_types import Language

# Test or normal app operation mode
TEST_APP_MODE = False


CURR_LANG = Language.ENGLISH  # selected language (Language.RUSSIAN or Language.ENGLISH)

# Endpoint for online university's api
API_URL = "https://b2b.itresume.ru/api/statistics"

# Getting environment variables
env = environ.Env()
environ.Env.read_env()

# Hidden API request parameters
REQ_CLIENT = env('client', str)
REQ_CLIENT_KEY = env('client_key', str)

# Logging system's parameters
LOGS_PATH = '.logs'             # Log's files path
MAX_NUM_LOGS_FILES = 3          # Maximum enabled number of log's files  ( acceptable >= 1 )#
LOG_EVERY_INCOMING_LINE = True  # If false, will be logging only for corrupt line

# Parameters for connection to local Postgres server
SERVER_CONNECTION_PARAMS = dict(host = 'localhost',
                                port = 5432,
                                dbname = 'postgres',
                                user = 'postgres',
                                password = '123456',
                                autocommit = False
                                )

# Parameters for working with main table
DB_MAIN_TABLE_NAME = 'lms_activities'    # Name of the main table of the database
DB_MAIN_TABLE_OPEN_RESET = False  # "True" means that every time the main table is opened, it will be reset


if __name__ == '__main__' :
    print(f"client: {env('client', str)}, client_key: {'#'*len(env('client_key', str))}")

