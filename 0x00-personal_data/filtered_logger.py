#!/usr/bin/env python3
"""Module that filters and obfuscates log message"""
import re
from typing import List


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
