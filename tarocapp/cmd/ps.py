from rich.live import Live
from time import sleep

from tarocapp import view


def run(args):
    jobs_view = view.create_job_view(2, 'Running Jobs')
    with Live(jobs_view) as live_view:
        sleep(1)
        r1 = ['host1', 'job1', 'instance1', '2012-09-02', '2012-09-02', '2h', 'RUNNING', '', 'Bla bla']
        jobs_view.add_host_rows('any', [r1])
        live_view.refresh()
        sleep(1)
        jobs_view.add_host_rows('any', [r1])
        live_view.refresh()
