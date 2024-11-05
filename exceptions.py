"""
The module for description own exceptions
"""


class ErrorInitLogsStorage(Exception) :
    """Failed to prepare for logging correctly"""
    ...


class ErrorMoreThanOneInstance(Exception) :
    """An attempt to create more than one instance of singleton-class"""
    ...

# class ApiServiceError(Exception):
#     """Program get API-service error"""
#     ...
