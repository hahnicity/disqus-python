class APIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '%s: %s' % (self.code, self.message)


class InterfaceNotDefined(NotImplementedError):
    def __init__(self):
        super(InterfaceNotDefined, self).__init__(
            'Interface is not defined, you must pass ``method`` (HTTP Method).'
        )


class InvalidAccessToken(APIError):
    pass


ERROR_MAP = {18: InvalidAccessToken}
