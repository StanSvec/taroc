from taroc.err import Error, ErrCode


class TarocAppError(Error):
    """Base-class for all exceptions raised by taroc application"""

    def __init__(self, code, *args):
        super().__init__(code, *args)
        self.code = code


class NoHosts(TarocAppError):

    def __init__(self):
        super(TarocAppError, self).__init__(ErrCode.NO_SSH_HOSTS, 'No hosts provided and SSH hosts file not found')

