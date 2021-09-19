import asyncio
from collections import namedtuple

import itertools
from rich.live import Live

import taroc
from taroc import hosts
from taroc.job import JobInstance
from tarocapp.err import InvalidExecutionError
from tarocapp.view import JobsView

COLUMNS = ['Host', 'Job ID', 'Instance ID', 'Created', 'Execution Time', 'State', 'Warnings',
           'Status (last output)']

Row = namedtuple('Row', 'host job_id instance_id created execution_time state warnings status')


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
    all_hosts = itertools.chain.from_iterable(group_to_hosts.values())
    host_to_task = taroc.ps(*all_hosts)
    jobs_view = JobsView(hosts_count=len(host_to_task), columns=COLUMNS)
    with Live(jobs_view) as live_view:
        for next_done in asyncio.as_completed(host_to_task.values()):
            host, jobs = await next_done
            rows = [_to_job_row(host, job) for job in jobs]
            jobs_view.add_host_rows(host, rows)
            live_view.refresh()


def _to_job_row(host, job: JobInstance):
    return Row(host, job.job_id, job.instance_id, job.created, job.execution_time, job.state, str(job.warnings),
               job.status)
