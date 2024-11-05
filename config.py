"""
The module for configuration.
"""

# The storage of private information is organized in the .env file of environment variables.
# The contents of the .env file for the correct operation of the application are closed API request parameters:
#   client=<client's name>
#   client_key=<client's key>


from datetime import datetime
import environ

# Endpoint for online university's api
API_URL = "https://b2b.itresume.ru/api/statistics"

# Getting environment variables
env = environ.Env()
environ.Env.read_env()

# API request parameters
REQ_CLIENT = env('client', str)
REQ_CLIENT_KEY = env('client_key', str)
REQ_START_TIME = datetime.fromisoformat('2023-04-01 00:00:00.000000')
REQ_END_TIME = datetime.fromisoformat('2023-04-01 00:01:59.999999')

# Logging system's parameters
LOGS_PATH = '.logs'         # Log's files path
MAX_NUM_LOGS_FILES = 3      # Maximum enabled number of log's files  ( acceptable >= 1 )

# Parameters for connection to local Postgres server
SERVER_CONNECTION_PARAMS = dict(host = 'localhost',
                                port = 5432,
                                database = 'postgres',
                                user = 'postgres',
                                password = '123456',
                                autocommit = False
                                )

# SERVER_PARAM_AUTOCOMMIT = False


# Language support
RUSSIAN = 0
ENGLISH = 1
CURR_LANG = ENGLISH  # selected language

# Language package of service messages
#
# data_processor module
AN_INVITATION_FOR_ENTERING_PROCESSING_DATE = (
                                'Введите дату извлечения данных в формате: <YYYY-mm-dd> или <exit> для выхода: ',
                                'Enter processing date in format: <<YYYY-mm-dd> or type <exit> for quit: ')
MESSAGE_ABOUT_BAD_INPUT = ('Ошибка ввода даты, попробуйте еще раз...', 'Bad input. Let\'s try again...')

# Logger's messages texts
LOG_STARTING_WORK_WITH_API = ('скачивание данных началось', 'beginning getting of data')
LOG_ENDING_WORK_WITH_API = ('скачивание данных завершено', 'ending getting of data')

LOG_STARTING_WORK_WITH_DBMS = ('загрузка данных в базу началась', 'the upload to the database has started')
LOG_ENDING_WORK_WITH_DBMS = ( 'загрузка данных в базу завершена', 'the upload to the database has ended')




if __name__ == '__main__' :
    print(f"client: {env('client', str)}, client_key: {'#'*len(env('client_key', str))}")

