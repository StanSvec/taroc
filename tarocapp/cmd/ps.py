from rich.live import Live
from time import sleep

from tarocapp.view import JobsView

COLUMNS = ['Host', 'Job ID', 'Instance ID', 'Created', 'Ended', 'Execution Time', 'State', 'Warnings',
           'Status (last output)']


def run(args):
    jobs_view = JobsView(hosts_count=2, table_title='Running Jobs', columns=COLUMNS)
    with Live(jobs_view) as live_view:
        sleep(1)
        r1 = ['host1', 'job1', 'instance1', '2012-09-02', '2012-09-02', '2h', 'RUNNING', '', 'Bla bla']
        jobs_view.add_host_rows('any', [r1])
        live_view.refresh()
        sleep(1)
        jobs_view.add_host_rows('any', [r1])
        live_view.refresh()
