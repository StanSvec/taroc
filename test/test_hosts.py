import textwrap
from pathlib import Path

import pytest

from taroc import hosts
from taroc.hosts import Include

HOSTS_FILE = 'test.hosts'


@pytest.fixture(autouse=True)
def remove_config_if_created():
    yield
    _remove_test_config_()


def _create_test_config(config):
    with open(HOSTS_FILE, 'w') as outfile:
        outfile.write(textwrap.dedent(config))


def _remove_test_config_():
    host_file = Path(HOSTS_FILE)
    if host_file.exists():
        host_file.unlink()


def test_no_hosts_specified_include_all():
    config = """\
        [all]
        host_a
        
        [default]
        host0
    
        [hosts1]
        host1
        
        [hosts2]
        host1
        host2
    """

    _create_test_config(config)
    name_to_hosts = hosts.read(HOSTS_FILE)

    assert {'all', 'default', 'hosts1', 'hosts2'} == set(name_to_hosts.keys())
    assert name_to_hosts['default'] == ['host0', 'host_a']
    assert name_to_hosts['hosts2'] == ['host1', 'host2', 'host_a']


def test_no_hosts_specified_include_default():
    config = """\
        [all]
        host_a
        
        [default]
        host0
    
        [hosts1]
        host1
    """

    _create_test_config(config)
    name_to_hosts = hosts.read(HOSTS_FILE, no_host_specified=Include.DEFAULT_ONLY)

    assert {'default'} == set(name_to_hosts.keys())
    assert name_to_hosts['default'] == ['host0', 'host_a']


def test_hosts_specified():
    config = """\
        [all]
        host_a
        
        [default]
        host0
    
        [hosts1]
        host1
        
        [hosts2]
        host1
        host2
    """

    _create_test_config(config)
    name_to_hosts = hosts.read(HOSTS_FILE, 'hosts1', 'hosts2')

    assert {'hosts1', 'hosts2'} == set(name_to_hosts.keys())
    assert name_to_hosts['hosts1'] == ['host1', 'host_a']
    assert name_to_hosts['hosts2'] == ['host1', 'host2', 'host_a']
