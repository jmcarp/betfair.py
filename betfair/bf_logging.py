# -*- coding: utf-8 -*-
__author__ = 'Ammar Akhtar'

"""
simple logging for betfair.py

heavily inspired by
    https://docs.python.org/2/howto/logging-cookbook.html,
    http://pymotw.com/2/logging/

"""

import logging
import logging.handlers

LOG_FILENAME = 'logs/logs.out'
formatter = logging.Formatter('%(levelname)s [%(asctime)s]'
                              '[%(name)s] [%(filename)s:%(lineno)s] %(message)s')

loghandler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                  maxBytes=1000000, backupCount=15)
loghandler.setFormatter(formatter)
loghandler.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

stream_logger = logging.getLogger('stream_logger')
stream_logger.addHandler(ch)

main_logger = logging.getLogger('betfair_logger')
main_logger.addHandler(loghandler)
main_logger.addHandler(ch)
main_logger.setLevel(logging.INFO)
