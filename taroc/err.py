from enum import Enum


class ErrCode(Enum):

    INVALID_CONFIG_SSH_DISABLED = 1

    INVALID_CONFIG_ATTR = 2

    NO_SSH_HOSTS = 3

    def __init__(self, code: int):
        self.code = code

    def __str__(self):
        return f"ERR{self.code}"


class Error(Exception):

    def __init__(self, code, *args):
        super().__init__(*args)
        self.code = code

    def __str__(self):
        if self.args:
            msg = self.args[0]
        elif self.__cause__:
            msg = str(self.__cause__)
        else:
            msg = '<details missing>'

        return f"{msg} (See {self.code} code in ERRORS.md in Github repo for more information," \
               f" use --debug for full stack)"
