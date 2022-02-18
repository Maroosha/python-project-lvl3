"This is __init__.py."

import logging
from page_loader.page_loader import download

__all__ = ('download',)

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'page_loader.log'


def do_log_config():
    "Configure logging."
    logging.basicConfig(
        filename=LOG_FILE,
        filemode='w',
        format=FORMAT,
        level=logging.DEBUG,
    )


do_log_config()
