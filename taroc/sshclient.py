import asyncio
import json
from dataclasses import dataclass
from typing import TypeVar, Callable, Generic, Awaitable, Optional

import asyncssh

from taroc import cfg, job
from taroc.job import JobInstances


@dataclass(frozen=True)
class HostInfo:
    """
    Information needed for communication with a host.
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
    resp_obj: Optional[T]
    success: bool = True
    error: Optional[Exception] = None

    @classmethod
    def error(cls, host, error):
        return cls(host, None, False, error)


def create_tasks(command: str, resp_deser: Callable[[HostInfo, str], T], *hosts: HostInfo) \
        -> dict[HostInfo, Awaitable[Response[T]]]:
    return {host_info: _exec(host_info, command, resp_deser) for host_info in hosts}


async def _exec(host_info: HostInfo, command: str, resp_deser: Callable[[HostInfo, str], T]) -> Response[T]:
    conn_task = asyncssh.connect(host_info.host, login_timeout=cfg.ssh_con_timeout)
    try:
        conn = await asyncio.wait_for(conn_task, cfg.ssh_con_timeout)
    except asyncio.TimeoutError as e:
        return Response.error(host_info.host, e)

    async with conn:
        response = await conn.run(f"python3 -m taroapp {command}", check=True, timeout=cfg.ssh_run_timeout)

    resp_str = response.stdout
    resp_obj: T = resp_deser(host_info, resp_str)
    return Response(host_info.host, resp_obj)


def ps(*hosts: HostInfo) -> dict[HostInfo, Awaitable[Response[JobInstances]]]:
    return create_tasks('ps -f json', _str_to_job_instances, *hosts)


def _str_to_job_instances(host_info: HostInfo, val: str) -> JobInstances:
    return job.dto_to_job_instances(host_info.host, json.loads(val))
