import email
import imaplib
import os
from dataclasses import dataclass
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime

from dotenv import load_dotenv

from src.config import (
    DATE_FORMAT,
    DATA_PATH,
    SENT_EMAILS_UID_FILENAME,
    UID_COLUMN_NAME,
)
from src.utils.csv_handler import CSVHandler
from src.utils.logging_config import logger

load_dotenv()


@dataclass
class Email:
    uid: str
    name: str
    address: str
    date: str
    subject: str


class EmailClient:
    _HOST = os.getenv('HOST')
    _LOGIN = os.getenv('LOGIN')
    _PASSWORD = os.getenv('PASSWORD')

    @staticmethod
    def _decode_mime_header(header_str: str):
        if header_str is None:
            return ''
        decoded_header = decode_header(header_str)[0]
        header_bytes, charset = decoded_header
        if charset:
            try:
                return header_bytes.decode(charset)
            except:
                return header_bytes.decode('cp1252')
        return header_bytes

    @staticmethod
    def _convert_date(date_str: str):
        if date_str:
            parsed_date = parsedate_to_datetime(date_str)
            return parsed_date.strftime(DATE_FORMAT)
        return date_str

    def _parse_email(self, email_data: list, bytes_uid: bytes) -> Email:
        uid = bytes_uid.decode('utf-8')
        email_message = email.message_from_bytes(email_data[0][1])
        subject = self._decode_mime_header(email_message.get('Subject'))
        parsed_address = parseaddr(email_message.get('From'))
        date = self._convert_date(email_message.get('Date'))
        name = self._decode_mime_header(parsed_address[0])
        address = parsed_address[1]
        return Email(
            uid=uid, subject=subject, date=date, name=name, address=address
        )

    def fetch_emails(self, date: str) -> list[Email]:
        csv_handler = CSVHandler(DATA_PATH / SENT_EMAILS_UID_FILENAME)

        emails = []
        with imaplib.IMAP4_SSL(self._HOST) as mail:
            mail.login(self._LOGIN, self._PASSWORD)
            mail.select('INBOX')
            result, uids = mail.uid(
                'search',
                None,
                f'SINCE {date}',
            )
            sent_uids = csv_handler.read_column(UID_COLUMN_NAME)
            if result != 'OK':
                raise Exception('Ошибка получения писем. Result is not OK')
            for uid in uids[0].split():
                if uid.decode('utf-8') not in sent_uids:
                    try:
                        result, email_data = mail.uid('fetch', uid, '(RFC822)')
                    except:
                        logger.exception(f'Ошибка получение письма {uid}')
                        continue
                    if result == 'OK' and email_data and email_data[0]:
                        try:
                            parsed_email_data = self._parse_email(
                                email_data, uid
                            )
                        except:
                            logger.exception(
                                f'Ошибка парсинга письма {email_data[0]}'
                            )
                            continue
                        logger.info(
                            f'Получено письмо imap {parsed_email_data}'
                        )
                        emails.append(parsed_email_data)

            return emails
