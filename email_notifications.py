"""
The email notifications module.
"""

from datetime import date
import logging

import ssl
import smtplib
from email.message import EmailMessage
from ssl import SSLContext

# App's modules
import config
from config import CURR_LANG, GOOGLE_SHEETS_REPORT_LINK, SENDER_EMAIL
from logger import Mylogger

EMAIL_MESSAGE_SUBJECT = ('Уведомление об обработке данных за: ',
                         'Notification of the processing of data for the date:')

EMAIL_MESSAGE_SUCCESS_MESSAGE = (f'Обработка данных за дату завершена, итоговая статистика по ссылке: {GOOGLE_SHEETS_REPORT_LINK}',
         f'Data processing for the date is completed, the final statistics are available at the link: {GOOGLE_SHEETS_REPORT_LINK}')

EMAIL_MESSAGE_NOT_COMPLETE_MESSAGE = (f'Обработка данных за дату завершена, Googl Sheets отчет НЕ ОБНОВЛЕН!',
                        f'Data processing for the date has been completed, Google Sheets report HAS NOT BEEN UPDATED!')


def send_email_notifications(logger: Mylogger, process_date: date, googl_sheets_result: bool) -> None :
    '''
    A function for performing mailing
    :param logger: a logger for recording history
    :param process_date: the date on which the processing is performed
    :param googl_sheets_result: A flag indicating whether there is an updated Google Sheets report
    :return: None
    '''

    msg = EmailMessage()

    # the text of the mail
    if googl_sheets_result :
        message = EMAIL_MESSAGE_SUCCESS_MESSAGE[CURR_LANG.value]
    else:
        message = EMAIL_MESSAGE_NOT_COMPLETE_MESSAGE[CURR_LANG.value]

    msg.set_content(message)

    msg['Subject'] = f'{EMAIL_MESSAGE_SUBJECT[CURR_LANG.value]} {process_date}'  # the subject of the mail
    msg['From'] = SENDER_EMAIL    # source email address
    msg['To'] = ', '.join(config.EMAIL_ADDRESSES_FOR_MAILING)   # list of email addresses for mailing

    # creating an SSL-connection with the SMTP-server
    try:
        # creating an SSL-context
        context: SSLContext = ssl.create_default_context()
    except Exception as err:
        logger.msg(logging.ERROR, f'Error creation SSL context: {err}')
        return

    try:
        # creating a connection
        smtp_server = config.SMTP_SERVER    # this is an SMTP-server
        port = config.SMTP_PORT             # the port for the SMTP-server
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)   # this is a connection
    except Exception as err:
        logger.msg(logging.ERROR, f'Error SMTP connection create: {err}')
        return

    try:
        # authorization on the SMTP-server
        sender_email = SENDER_EMAIL     # sender_email - source email address
        password = config.SMTP_PASSWORD     # special password
        server.login(sender_email, password)    # trying to connect to the server
    except Exception as err:
        logger.msg(logging.ERROR, f'SMTP Server login error: {err}')
        return

    try:
        # sending an email message
        server.send_message(msg=msg)
        server.quit()
        # The final mark in the journal on the successful sending of the email notifications
        logger.msg_mailing_success_completed()

    except Exception as err:
        logger.msg(logging.ERROR, f'Error sending mail: {err}')


if __name__ == "__main__":
    # test run
    test_date = date(2024, 10, 2)
    logger = Mylogger(test_date)
    send_email_notifications(logger, test_date)
