class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ReferencesNotFoundError(Error):
    """Exception raised for errors like not find the
    References keywor.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        self.message = "Unable to find References keyword"

