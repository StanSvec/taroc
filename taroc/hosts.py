"""
Hosts file can have these sections (host groups):
[default] - hosts in this group are used when requested or when no groups are specified
[all] - hosts in this group are added to all existing hosts sections
[{custom}] - hosts in this group are used when requested or when no groups are specified and configured this way
"""

import configparser
from enum import Enum, auto
from typing import List

from taroc import paths


class Include(Enum):
    DEFAULT_ONLY = auto()
    ALL = auto()


def read_ssh_hosts_file(*groups, no_group=Include.ALL):
    """Returns dictionary of (host_group, hosts) entries from SSH hosts file
    :param groups: host groups to include
    :param no_group: behaviour when no host groups are provided
    :return: (host_group, hosts) dict
    :raise FileNotFoundError: when SSH hosts file cannot be found
    """
    return read_file(paths.SSH_HOSTS, *groups, no_group=no_group)


def read_file(hosts_file, *groups, no_group=Include.ALL) -> dict[str, List[str]]:
    """Returns dictionary of {host_group to hosts} entries from provided hosts file
    :param hosts_file: ini file with sections representing host groups
    :param groups: host groups to include
    :param no_group: behaviour when no host groups are provided
    :return: host_group to hosts dict
    :raise FileNotFoundError: when hosts file cannot be found
    """
    hosts_file_path = paths.lookup_file_in_config_path(hosts_file)
    config = configparser.ConfigParser(allow_no_value=True, default_section='all')
    config.read(hosts_file_path)

    return {hosts_section: list(config[hosts_section]) for hosts_section in config
            if hosts_section in groups or
            not groups and (no_group == Include.ALL or hosts_section == 'default')}
