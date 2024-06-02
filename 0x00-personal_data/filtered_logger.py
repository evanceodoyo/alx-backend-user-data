#!/usr/bin/env python3
"""Module that filters and obfuscates log message"""
import os
import re
import logging
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect and return database connector object"""
    usr = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    hst = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db = os.getenv("PERSONAL_DATA_DB_NAME")
    cnx = mysql.connector.connect(
        user=usr,
        password=pwd,
        host=hst,
        database=db
    )
    return cnx


def get_logger() -> logging.Logger:
    """Create and return a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Filters and returns log message obfuscated.

    Args:
      fields (List of strings): reprents all fileds to obfuscate.
      redaction (str): represents what field to be obfuscated.
      message (str): represents the log line.
      separator (str): represents character by which to separate
      all the fields in the log line.
    """
    return re.sub(
        f'({"|".join(fields)})=[^{separator}]+',
        lambda m: f"{m.group().split('=')[0]}={redaction}",
        message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter incoming logs"""
        return filter_datum(
            self.fields,
            RedactingFormatter.REDACTION,
            super(RedactingFormatter, self).format(record),
            RedactingFormatter.SEPARATOR
        )


def main() -> None:
    """main function"""
    cnx = get_db()
    info_logger = get_logger()
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = f"SELECT {fields} FROM users;"

    with cnx.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda m: f"{m[0]}={m[1]}",
                zip(columns, row)
            )
            msg = f"{('; '.join(list(record)))}"
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


if __name__ == "__main__":
    main()
