# -*- coding: utf-8 -*-
from . import bf_logging

class BetfairError(Exception):
    def __init__(self, message):
        bf_logging.main_logger.exception(message)
        # pass
    pass


class BetfairLoginError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        self.message = data.get('loginStatus', 'UNKNOWN')
        super(BetfairLoginError, self).__init__(self.message)


class BetfairAuthError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        self.message = data.get('error', 'UNKNOWN')
        super(BetfairAuthError, self).__init__(self.message)


class BetfairAPIError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        try:
            error_data = data['error']['data']['APINGException']
            self.message = error_data.get('errorCode', 'UNKNOWN')
            self.details = error_data.get('errorDetails')
        except KeyError:
            self.message = 'UNKNOWN'
            self.details = None
        super(BetfairAPIError, self).__init__(self.message)
