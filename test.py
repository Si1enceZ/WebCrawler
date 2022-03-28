import threading
import time
import logging
from script.core import get_page
if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(pathname)s - line: %(lineno)d - %(funcName)s - %(message)s"
    logging.basicConfig(filename='Tenda/test.log', level='DEBUG', format=LOG_FORMAT)

    get_page('123')
    logging.debug('This a debug log')
    logging.info('This a info log')
    logging.warning('This a warning log')
    logging.error('This a error log')
    logging.critical('This a critical log')
