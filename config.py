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

# Test or normal app operation mode
TEST_APP_MODE = False

# Logging system's parameters
LOGS_PATH = '.logs'         # Log's files path
MAX_NUM_LOGS_FILES = 3      # Maximum enabled number of log's files  ( acceptable >= 1 )

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
DB_SIZE_BUFF_FOR_UPLOAD = 100   # A size buffer for upload data in main table (in lines)

# Language support
RUSSIAN = 0
ENGLISH = 1
CURR_LANG = RUSSIAN  # selected language

# Language package of service messages
#
# data_processor module
AN_INVITATION_FOR_ENTERING_PROCESSING_DATE = (
    'Введите дату извлечения/загрузки данных в формате: <YYYY-mm-dd> или <exit> для выхода: ',
    'Enter processing date in format: <<YYYY-mm-dd> or type <exit> for quit: '
)
MESSAGE_ABOUT_BAD_INPUT = (
    'Ошибка ввода даты, попробуйте еще раз...',
    'Bad input. Let\'s try again...'
)

# Logger's messages texts
LOG_STARTING_WORK_WITH_API = (
    ('начинаем сбор данных за ', ' с: ', ' по: '),
    ('we start collecting data for ', ' from: ', ' to: ')
)
LOG_ENDING_WORK_WITH_API = (
    'завершено скачивание данных за ',
    'data download completed for '
)
LOG_TOTAL_NUM_LINES_API = (
    ('общее количество прочитанных строк: ', ', в том числе ', ' успешно, ', ' испорчено'),
    ('total number of lines read: ', ' including ', ' successfully, ', ' is corrupted')
)

LOG_STARTING_WORK_WITH_DBMS = (
    'загрузка данных в базу началась',
    'the upload to the database has started'
)
LOG_ENDING_WORK_WITH_DBMS = (
    'загрузка данных в базу завершена',
    'the upload to the database has ended'
)
LOG_TOTAL_NUM_LINES_DBMS = (
    ('общее количество добавленных строк: ', ', в том числе ', ' с дефектами'),
    ('total number of added lines: ', ', including ', ' with defects')
)

LOG_IT_WAS_READ = (
    ('строка № ', ' прочитана: '),
    ('line # ', ' was read: ')
)
LOG_ERROR_READ = (
    ('строка № ', ' не прочитана - ошибка - отсутствует идентификатор <lti_user_id>'),
    ('line # ', ' wasn\'t read - error - the <lti_user_id> id is missing: ')
)

LOG_OMISSION_IN_THE_DATA = (
    ' пропущено значение поля: ',
    ' value of the field is missing: '
)
LOG_INCORRECT_COMBINATION_OF_PARAMETERS = (
    ' некорректное сочетание значений полей: ',
    ' incorrect combination of parameters: '
)
LOG_ERROR_IN_THE_DATA = (
    ('строка ', ', есть ошибки:'),
    ('line ', ', there are errors:')
)

if __name__ == '__main__' :
    print(f"client: {env('client', str)}, client_key: {'#'*len(env('client_key', str))}")

