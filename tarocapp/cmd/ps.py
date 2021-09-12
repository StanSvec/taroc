import asyncio

from rich.live import Live

import taroc
from tarocapp.view import JobsView

COLUMNS = ['Host', 'Job ID', 'Instance ID', 'Created', 'Ended', 'Execution Time', 'State', 'Warnings',
           'Status (last output)']


def run(args):
    asyncio.run(run_ps(args))


async def run_ps(args):
    host_to_task = taroc.ps('ciserver')
    jobs_view = JobsView(hosts_count=len(host_to_task), table_title='Running Jobs', columns=COLUMNS)
    with Live(jobs_view) as live_view:
        for next_done in asyncio.as_completed(host_to_task.values()):
            host_instances = await next_done
            rows = [_instance_to_row(inst) for inst in host_instances[1]]
            jobs_view.add_host_rows(host_instances[0], rows)
            live_view.refresh()


def _instance_to_row(inst):
    return ['host1', inst['job_id'], 'instance1', '2012-09-02', '2012-09-02', '2h', 'RUNNING', '', 'Bla bla']
