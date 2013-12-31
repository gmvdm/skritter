# -*- coding: utf-8 -*-


class RequestException(IOError):
    """There was an unforseen error that occurred while handling
    your request."""


class ConnectionError(RequestException):
    """A connection error occurred."""
