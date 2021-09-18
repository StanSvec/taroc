class TarocAppError(Exception):
    """Base-class for all exceptions raised by taroc application"""


class InvalidExecutionError(TarocAppError):
    """
    The application has been executed incorrectly.
    This can be mix of incompatible arguments, missing files, etc.
    """
