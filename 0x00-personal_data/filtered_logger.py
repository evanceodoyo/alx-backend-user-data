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
    return mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        port=3306
    )


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
