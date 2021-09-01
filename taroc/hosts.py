"""
Hosts file can have these sections:
[default] - hosts in this section are used when specified or when no hosts are specified
[all] - hosts in this section are added to all existing hosts sections
[{custom}] - hosts in this section are used when specified or when no hosts are specified if configured this way
"""

import configparser
from enum import Enum, auto
from typing import List

from taroc import paths


class Include(Enum):
    DEFAULT_ONLY = auto()
    ALL = auto()


def read(hosts_file, no_host_specified=Include.ALL, *hosts) -> dict[str, List[str]]:
    hosts_file_path = paths.lookup_file_in_config_path(hosts_file)
    config = configparser.ConfigParser(allow_no_value=True, default_section='all')
    config.read(hosts_file_path)

    return {hosts_section: list(config[hosts_section]) for hosts_section in config
            if hosts_section in hosts or
            not hosts and (no_host_specified == Include.ALL or hosts_section == 'default')}
