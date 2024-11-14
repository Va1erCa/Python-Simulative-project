"""
The module for Google Sheets report interaction.
"""

import gspread
from gspread import exceptions
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date

from app_types import DatabaseConnection


def calculate_values() :
    ...


def to_ordinal_googl_sheet_date(python_date: date) -> int:
    return python_date.toordinal() - datetime(1900, 1, 1).toordinal() + 2


def create_google_sheets_report(database_connection: DatabaseConnection|None, report_date: date) -> str:

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']

    # Reading Credentails from ServiceAccount Keys file
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Va1erCaSimulativeOnCloudProject-2-434909.json'
                , scope)

    # intitialize the authorization object
    gc = gspread.authorize(credentials)
    # print(gc.list_spreadsheet_files())

    # Open Google Sheets file
    sheets = gc.open('Отчет об успеваемости студентов')

    try:
        sheet = sheets.sheet1   # Getting sheet for preparing our report

        # rows = sheet.get_values()
        # for r in rows: print(r)

        sheet.clear()   # Erasing the old data in our sheet
        report_template = [
            ['Сводная статистика по успеваемости за:', '', '', to_ordinal_googl_sheet_date(report_date)],
            ['Всего уникальных пользователей ', '', '', 999],
            ['Всего запусков (run):', '', '', 999],
            ['Всего попыток (submits):', '', '', 999],
            ['', 'в т.ч. успешных:', '', 999],
            ['', '% успешных:', '', 0.09],
            ['Среднее число попыток на 1го студента:', '', '', 99]
        ]

        # Creating a report framework
        sheet.append_rows(report_template)
        sheet.format(['D1'], {'numberFormat' : { 'type' : 'DATE', 'pattern' : 'dd.mm.yyyy'  } })
        sheet.format(['D6'], {'numberFormat' : { 'type' : 'PERCENT'}})

        # sheet.update_acell()('D1',  ) format('D1:D1', {''})
        # print(sheet.get_all_records())
        #
        # # append one
        # sheet.append_row(['4', 'Geography', 'A+'])
        # print(sheet.get_all_values())
        #
        # # updating
        # sheet.update([['Biology']], 'B5:B5')
        # sheet.update_acell('B2', 'Science')
        # sheet.update_cell(6, 2, 'Science')
        #
        # print(sheet.get_all_values())
    except Exception as e:
        print(f'Error Occurred {e}')

    return ''


if __name__ == "__main__":

    dt = date(2024, 11, 1)
    create_google_sheets_report(None, dt)



# ['Сводная статистика по успеваемости за:', '', '', '02.10.2024']
# ['Всего уникальных пользователей ', '', '', '55']
# ['Всего запусков (run):', '', '', '2500']
# ['Всего попыток (submits):', '', '', '2000']
# ['', 'в т.ч. успешных:', '', '1205']
# ['', '% успешных:', '', '60,25%']
# ['Среднее число попыток на 1го студента:', '', '', '36,36']