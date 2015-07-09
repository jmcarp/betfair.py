# -*- coding: utf-8 -*-


class BetfairError(Exception):
    pass


class NotLoggedIn(BetfairError):
    pass


class LoginError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        self.status_code = response.status_code
        self.message = data.get('loginStatus', 'UNKNOWN')
        super(LoginError, self).__init__(self.message)


class AuthError(BetfairError):

    def __init__(self, response, data):
        self.response = response
        self.status_code = response.status_code
        self.message = data.get('error', 'UNKNOWN')
        super(AuthError, self).__init__(self.message)


class ApiMetaError(BetfairError):

    def __init__(self, response, message, details):
        self.response = response
        self.status_code = response.status_code
        self.message = message
        self.details = details
        super(ApiMetaError, self).__init__(self.message)


class ApiError(ApiMetaError):

    def __init__(self, response, data):
        try:
            error_data = data['error']['data']['APINGException']
            message = error_data.get('errorCode', 'UNKNOWN')
            details = error_data.get('errorDetails')
        except KeyError:
            message = 'UNKNOWN'
            details = None
        super(ApiError, self).__init__(response, message, details)


class ApiHttpError(ApiMetaError):

    def __init__(self, response):
        super(ApiHttpError, self).__init__(response, "error http return code: %s" %
                                           response.status_code, None)
