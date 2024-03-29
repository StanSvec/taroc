"""Global configuration

Implementation of config pattern:
https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
"""

import distutils.util
import sys

# ------------ DEFAULT VALUES ------------ #
from taroc.err import Error, ErrCode

DEF_SSH_CONFIG_ENABLED = True
DEF_SSH_CON_TIMEOUT = 5
DEF_SSH_RUN_TIMEOUT = 5

DEF_THEME = ''

DEF_STATUS_MAX_LENGTH = 500

# ------------ CONFIG VALUES ------------ #
ssh_config_enabled = DEF_SSH_CONFIG_ENABLED
ssh_con_timeout = DEF_SSH_CON_TIMEOUT
ssh_run_timeout = DEF_SSH_RUN_TIMEOUT

theme = DEF_THEME

status_max_length = DEF_STATUS_MAX_LENGTH


def set_variables(**kwargs):
    module = sys.modules[__name__]
    for name, value in kwargs.items():
        try:
            cur_value = getattr(module, name)
        except AttributeError as e:
            raise InvalidConfigAttribute from e

        if type(value) == type(cur_value):
            value_to_set = value
        elif isinstance(cur_value, bool):  # First bool than int, as bool is int..
            value_to_set = distutils.util.strtobool(value)
        elif isinstance(cur_value, int):
            value_to_set = int(value)
        else:
            raise ValueError(f'Cannot convert value {value} to {type(cur_value)}')

        setattr(module, name, value_to_set)


class InvalidConfig(Error):

    def __init__(self, code, *args):
        super(InvalidConfig, self).__init__(code, *args)


class InvalidConfigAttribute(Error):

    def __init__(self, *args):
        super(InvalidConfigAttribute, self).__init__(ErrCode.INVALID_CONFIG_ATTR, *args)
