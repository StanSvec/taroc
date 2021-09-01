"""
Hosts file can have these sections:
[default] - hosts in this section are used when specified or when no hosts are specified
[all] - hosts in this section are added to all existing hosts sections
[{custom}] - hosts in this section are used when specified or when no hosts are specified if configured this way
"""

import configparser
from typing import List

from taroc import paths


def read(hosts_file, *hosts) -> dict[str, List[str]]:
    hosts_file_path = paths.lookup_file_in_config_path(hosts_file)
    config = configparser.ConfigParser(allow_no_value=True, default_section='all')
    config.read(hosts_file_path)

    return {hosts_section: list(config[hosts_section]) for hosts_section in config}
