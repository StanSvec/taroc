from typing import List, Awaitable

from taroc import cfgfile, paths, cfg, sshclient
from taroc.job import JobInstance
from taroc.sshclient import HostInfo, Response


def load_defaults(**kwargs):
    cfgfile.load_default()
    setup(**kwargs)


def load_config(config=None, **kwargs):
    cfgfile.load(config)
    setup(**kwargs)


def setup(**kwargs):
    cfg.set_variables(**kwargs)


def ps(*hosts: HostInfo) -> dict[HostInfo, Awaitable[Response[List[JobInstance]]]]:
    return sshclient.ps(*hosts)
