# -*- coding: utf-8 -*-


class BetfairError(Exception):
    pass


class NotLoggedIn(BetfairError):
    pass


class LoginError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        self.message = data.get('loginStatus', 'UNKNOWN')
        super(LoginError, self).__init__(self.message)


class AuthError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        self.message = data.get('error', 'UNKNOWN')
        super(AuthError, self).__init__(self.message)


class ApiError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        try:
            error_data = data['error']['data']['APINGException']
            self.message = error_data.get('errorCode', 'UNKNOWN')
            self.details = error_data.get('errorDetails')
        except KeyError:
            self.message = 'UNKNOWN'
            self.details = None
        super(ApiError, self).__init__(self.message)
