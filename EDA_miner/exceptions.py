"""
This module contains custom exceptions, simply to help with debugging and \
logging. This is still experimental.
"""


class UnexpectedResponse(Exception):
    """
    Created primarily to inform about failed requests to (REST) APIs.
    """
    pass
