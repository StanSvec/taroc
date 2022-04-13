from typing import Awaitable

from taroc import cfgfile, paths, cfg, sshclient
from taroc.err import ErrCode
from taroc.job import JobInstance, JobInstances
from taroc.sshclient import HostInfo, Response


def load_defaults(**kwargs):
    cfgfile.load_default()
    setup(**kwargs)


def load_config(config=None, **kwargs):
    cfgfile.load(config)
    setup(**kwargs)


def setup(**kwargs):
    cfg.set_variables(**kwargs)
    if not cfg.ssh_config_enabled:
        raise cfg.InvalidConfig(ErrCode.INVALID_CONFIG_SSH_DISABLED, 'SSH must be enabled')
        # At the moment only SSH communication is implemented


def ps(*hosts: HostInfo) -> dict[HostInfo, Awaitable[Response[JobInstances]]]:
    return sshclient.ps(*hosts)
