import logging
from datetime import datetime


def configure_logging(file_id):
    logging.basicConfig(filename=get_config_file_name(file_id), level=logging.DEBUG)


def get_config_file_name(file_id):
    return f"logs/{datetime.now().strftime('%Y%m%d%H%M%S')}-{file_id}.log"


def log(content):
    logging.debug(content)
