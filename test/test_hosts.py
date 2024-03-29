import pytest

from taroc import hosts
from taroc.hosts import Include
from test import util

HOSTS_FILE = 'test.hosts'


@pytest.fixture(autouse=True)
def remove_config_if_created():
    yield
    util.remove_test_file(HOSTS_FILE)


def create_test_file(content):
    util.create_test_file(HOSTS_FILE, content)


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

    create_test_file(config)
    group_to_hosts = hosts.read_file(HOSTS_FILE)

    assert {'all', 'default', 'hosts1', 'hosts2'} == set(group_to_hosts.keys())
    assert group_to_hosts['default'] == ['host0', 'host_a']
    assert group_to_hosts['hosts2'] == ['host1', 'host2', 'host_a']


def test_no_hosts_specified_include_default():
    config = """\
        [all]
        host_a
        
        [default]
        host0
    
        [hosts1]
        host1
    """

    create_test_file(config)
    group_to_hosts = hosts.read_file(HOSTS_FILE, no_group=Include.DEFAULT_ONLY)

    assert {'default'} == set(group_to_hosts.keys())
    assert group_to_hosts['default'] == ['host0', 'host_a']


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

    create_test_file(config)
    group_to_hosts = hosts.read_file(HOSTS_FILE, 'hosts1', 'hosts2')

    assert {'hosts1', 'hosts2'} == set(group_to_hosts.keys())
    assert group_to_hosts['hosts1'] == ['host1', 'host_a']
    assert group_to_hosts['hosts2'] == ['host1', 'host2', 'host_a']
