import asyncio

import itertools
from rich.live import Live

import taroc
from taroc import hosts
from tarocapp.view import JobsView

COLUMNS = ['Host', 'Job ID', 'Instance ID', 'Created', 'Ended', 'Execution Time', 'State', 'Warnings',
           'Status (last output)']


def run(args):
    asyncio.run(run_ps(args))


async def run_ps(args):
    try:
        group_to_hosts = hosts.read_ssh_hosts()
    except FileNotFoundError:
        print('SSH hosts file not found')
        exit(-1)
        return  # To remove the assignment warning

    all_hosts = itertools.chain.from_iterable(group_to_hosts.values())
    host_to_task = taroc.ps(*all_hosts)
    jobs_view = JobsView(hosts_count=len(host_to_task), columns=COLUMNS)
    with Live(jobs_view) as live_view:
        for next_done in asyncio.as_completed(host_to_task.values()):
            host, jobs = await next_done
            rows = [_to_job_row(host, job) for job in jobs]
            jobs_view.add_host_rows(host, rows)
            live_view.refresh()


def _to_job_row(host, job):
    return [host, job['job_id'], 'instance1', '2012-09-02', '2012-09-02', '2h', 'RUNNING', '', 'Bla bla']
