class CommunicatorNotFound(Exception):
    pass


class CommunicatorAuthenticationFailed(Exception):
    pass


class CommandNotImplementedError(BaseException):
    pass


class GenieCommandMissingError(BaseException):
    pass


class SNMPCommandOIDMissingError(BaseException):
    pass