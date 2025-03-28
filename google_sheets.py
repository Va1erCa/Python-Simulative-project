"""
The module for Google Sheets report interaction.
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import logging
import psycopg2
from datetime import datetime, date

from put_data import DatabaseConnection
from logger import Mylogger
from app_types import Report
import config
from config import CURR_LANG


# The main request for the preparation of the Google sheets report
REPORT_MAIN_QUERY = \
    '''
        with rep_day as (
            select	user_id, created_at::date as created_at, is_correct, attempt_type 
        from '''+config.DB_MAIN_TABLE_NAME+''' 
        where created_at::date = %s )
        select 
            'total_unique_users' as rep_param_name, 
            count(distinct user_id) as rep_param_value 
        from rep_day 
        union
        select 
            'total_runs' as rep_param_name, 
            count(*) as rep_param_value
        from rep_day
        where attempt_type = 'run'
        union
        select 
            'total_submits' as rep_param_name, 
            count(*) as rep_param_value
        from rep_day   
        where attempt_type = 'submit'
        union
        select 
            'total_success_submits' as rep_param_name, 
            count(*) as rep_param_value
        from rep_day   
        where attempt_type = 'submit' and is_correct
    '''

REPORT_TEMPLATE = (
    (('Сводная статистика по успеваемости за:', '', '', '99.99.9999'),
     ('Всего уникальных пользователей:', '', '', 999),
     ('Всего запусков (run):', '', '', 999),
     ('Всего попыток (submits):', '', '', 999),
     ('', 'в т.ч. успешных:', '', 999),
     ('', '% успешных:', '', 99.9),
     ('Среднее число попыток на 1го студента:', '', '', 99),
     ('Среднее число успешных попыток на 1го:', '', '', 99),
     ('', '', '', ''),
     ('Отчет подготовлен:', '', '', '99.99.9999')
     ),
    (('Final performance data for for:', '', '', '99.99.9999'),
     ('Total unique users:', '', '', 999),
     ('Total code runs (run):', '', '', 999),
     ('Total submits (submits):', '', '', 999),
     ('', 'including successfully:', '', 999),
     ('', '% successfully:', '', 99.9),
     ('Average number of submits per 1st student:', '', '', 99),
     ('Average number of successful per student:', '', '', 99),
     ('', '', '', ''),
     ('The report has been prepared:', '', '', '99.99.9999')
     )
)


def to_ordinal_googl_sheet_date(python_date: date) -> int:
    '''
    Date-to-integer conversion function for use in Google Sheets
    :param python_date: this is a date in python format
    :return: date in integer format
    '''
    return python_date.toordinal() - datetime(1900, 1, 1).toordinal() + 2


def calculate_values_for_report(logger: Mylogger, db_connection: DatabaseConnection, report_date:date) -> Report| None :
    '''
    A function that calculates the values needed for the report
    :param logger: a logger for recording history
    :param db_connection: DatabaseConnection - object
    :param report_date: the date on which the processing is performed
    :return: report data in the format Report class
    '''

    # A dictionary for storing four values that we get from the database when executing the main query
    rep_part = dict(total_unique_users=0,
                    total_runs=0,
                    total_submits=0,
                    total_success_submits=0)

    connection = db_connection.get_connection()
    try :
        with connection :
            with connection.cursor() as cursor :
                cursor.execute(REPORT_MAIN_QUERY, (report_date.strftime('%Y-%m-%d'),))
                for r in cursor.fetchall() :
                    rep_part[r[0]] = r[1]   # saving in the dictionary our values from the database

    except psycopg2.Error as err :
        logger.msg_error_get_rep_information(err)
        return None

    rep = Report(to_ordinal_googl_sheet_date(report_date),
                 rep_part['total_unique_users'],
                 rep_part['total_runs'],
                 rep_part['total_submits'],
                 rep_part['total_success_submits'],
                 round(rep_part['total_success_submits']/rep_part['total_submits'],1),
                 round(rep_part['total_submits'] / rep_part['total_unique_users'], 0),
                 round(rep_part['total_success_submits'] / rep_part['total_unique_users'], 0),
                 '',
                 to_ordinal_googl_sheet_date(datetime.now().date())
                 )

    return rep


def create_google_sheets_report(logger: Mylogger, db_connection: DatabaseConnection, report_date: date) -> bool:
    '''

    :param logger: a logger for recording history
    :param db_connection: DatabaseConnection - object
    :param report_date: the date on which the processing is performed
    :return: a boolean value equal to "True" when the report sheet is successfully created
    '''

    # The initial mark in the journal about the preparation of the report
    logger.msg_google_sheets_start()

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']

    # Reading Credentials from ServiceAccount Keys file
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Va1erCaSimulativeOnCloudProject-2-434909.json'
                , scope)

    # intitialize the authorization object
    gc = gspread.authorize(credentials)
    # Open Google Sheets file
    sheets = gc.open('Отчет об успеваемости студентов')
    try:
        sheet = sheets.sheet1   # Getting sheet for preparing our report
        sheet.clear()   # Erasing the old data in our sheet

        # Creating a report framework
        sheet.append_rows(REPORT_TEMPLATE[CURR_LANG.value])

        # Calculating values
        report_values = calculate_values_for_report(logger, db_connection, report_date)
        if report_values is not None :
            report_column = [[el] for el in report_values]

            sheet.update(report_column,'D1:D10')

            sheet.format(['D1'], {'numberFormat' : {'type' : 'DATE', 'pattern' : 'dd.mm.yyyy'}})
            sheet.format(['D10'], {'numberFormat' : {'type' : 'DATE', 'pattern' : 'dd.mm.yyyy'}})
            sheet.format(['D6'], {'numberFormat' : {'type' : 'PERCENT'}})

            # The final mark in the journal on the successful preparation of the report
            logger.msg_google_sheets_success_end()
            return True

        else :
            return False

    except Exception as err:
        logger.msg(logging.ERROR, f'Error Occurred {err}')

    return False


if __name__ == "__main__":
    # test run
    test_date = date(2024, 10, 2)
    logger = Mylogger(test_date)
    db_connection = DatabaseConnection()
    create_google_sheets_report(logger, db_connection, test_date)