import argparse
import logging
from datetime import datetime
from pathlib import Path

LOGGING_ENABLED = False


def configure_file_logging(file_id):
    """
    Configures the logger to log to a file.

    :param file_id: An id to append to the file name. Useful when you run the same code but you want identifiable log files.
    :return: None
    """
    global LOGGING_ENABLED

    if __is_logging_enabled__():
        LOGGING_ENABLED = True
        Path("./logs").mkdir(exist_ok=True)
        logging.basicConfig(filename=__get_logging_file_name__(file_id), level=logging.DEBUG)


def log(content):
    """
    Logs the content to file. You must call configure_file_logging before using log.

    :param content: Anything that can be represented as a string
    :return: None
    """
    global LOGGING_ENABLED
    if LOGGING_ENABLED:
        logging.debug(content)


def __is_logging_enabled__():
    """
    Get the --logging argument

    :return: bool
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--logging", help="Activate logging", default=False)

    return parser.parse_args().logging


def __get_logging_file_name__(file_id):
    """
    Composes a logging file name. It contains a timestamp followed by a file id.
    Example: 20210306113741-MyBot-2.log

    :param file_id: An id to append to the file name. Useful when you run the same code but you want identifiable log files.
    :return: str
    """
    return f"logs/{datetime.now().strftime('%Y%m%d%H%M%S')}-{file_id}.log"
