import asyncio

import itertools
from rich.live import Live

import taroc
from taroc import hosts, HostInfo
from tarocapp.err import InvalidExecutionError
from tarocapp.model import JobInstancesModel
from tarocapp.view import JobColumns as Col, JobInstancesView

COLUMNS = [Col.HOST, Col.JOB_ID, Col.INSTANCE_ID, Col.CREATED, Col.TIME, Col.STATE, Col.WARNINGS, Col.STATUS]


def run(args):
    group_to_hosts = _group_to_hosts(args)
    asyncio.run(run_ps(group_to_hosts))


def _group_to_hosts(args):
    if args.host:
        return {'cli_args': args.host}

    try:
        return hosts.read_ssh_hosts()
    except FileNotFoundError:
        raise InvalidExecutionError('No hosts provided and SSH hosts file not found')


async def run_ps(group_to_hosts):
    all_hosts = [HostInfo(host) for host in itertools.chain.from_iterable(group_to_hosts.values())]
    host_to_task = taroc.ps(*all_hosts)
    jobs_model = JobInstancesModel(len(host_to_task))
    jobs_view = JobInstancesView(COLUMNS, jobs_model)
    with Live(jobs_view):
        for next_done in asyncio.as_completed(host_to_task.values()):
            response = await next_done
            if response.success:
                jobs_model.add_host_jobs(response.host, response.resp_obj)
            else:
                jobs_model.add_host_error(response.host, response.error)
