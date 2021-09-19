import json
from dataclasses import dataclass

import asyncssh

from taroc import cfg, job


@dataclass(frozen=True)
class HostInfo:
    """This must be move to more generic module when more network protocols are supported"""

    host: str


def create_tasks(command, resp_deser, *hosts):
    return {HostInfo(host): _exec(host, command, resp_deser) for host in hosts}


async def _exec(host, command, resp_deser):
    async with asyncssh.connect(host, login_timeout=cfg.ssh_con_timeout) as conn:
        result = await conn.run(f"python3 -m taroapp {command}", check=True, timeout=cfg.ssh_run_timeout)
        result_str = result.stdout
        resp = resp_deser(result_str)
        return host, resp


def ps(*hosts):
    return create_tasks('ps -f json', _str_to_job_instances, *hosts)


def _str_to_job_instances(val):
    return [job.dto_to_job_instance(as_dict) for as_dict in json.loads(val)]
