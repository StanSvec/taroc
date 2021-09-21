import json
from dataclasses import dataclass
from typing import TypeVar, Callable, Generic, List, Awaitable

import asyncssh

from taroc import cfg, job
from taroc.job import JobInstance


@dataclass(frozen=True)
class HostInfo:
    """
    Host information available before communicating with the host.

    Note: This must be moved to more generic module when more network protocols are supported.
    """

    host: str


T = TypeVar("T")


@dataclass(frozen=True)
class Response(Generic[T]):
    """
    Response data.

    Note: This must be moved to more generic module when more network protocols are supported.
    """

    host: str
    body_obj: T


def create_tasks(command: str, resp_deser: Callable[[str], T], *hosts: HostInfo) \
        -> dict[HostInfo, Awaitable[Response[T]]]:
    return {host_info: _exec(host_info, command, resp_deser) for host_info in hosts}


async def _exec(host_info: HostInfo, command: str, resp_deser: Callable[[str], T]) -> Response[T]:
    async with asyncssh.connect(host_info.host, login_timeout=cfg.ssh_con_timeout) as conn:
        result = await conn.run(f"python3 -m taroapp {command}", check=True, timeout=cfg.ssh_run_timeout)
        result_str = result.stdout
        resp_body: T = resp_deser(result_str)
        return Response(host_info.host, resp_body)


def ps(*hosts: HostInfo) -> dict[HostInfo, Awaitable[Response[List[JobInstance]]]]:
    return create_tasks('ps -f json', _str_to_job_instances, *hosts)


def _str_to_job_instances(val: str) -> List[JobInstance]:
    return [job.dto_to_job_instance(as_dict) for as_dict in json.loads(val)]
