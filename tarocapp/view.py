from dataclasses import dataclass
from typing import Callable, Any

from rich import box
from rich.console import Group, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeElapsedColumn
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from taroc import JobInstance, util


@dataclass(frozen=True)
class JobColumn:
    name: str
    job_to_column_val: Callable[[JobInstance], Any]
    val_to_render: Callable[[Any], RenderableType] = lambda val: str(val) if val is not None else ''


def _print_dict(dct):
    return ','.join(f"{k}:{v}" for k, v in dct)


class JobColumns:
    HOST = JobColumn('Host', lambda job: job.host)
    JOB_ID = JobColumn('Job ID', lambda job: job.job_id)
    INSTANCE_ID = JobColumn('Instance ID', lambda job: job.instance_id)
    CREATED = JobColumn('Created', lambda job: job.created, util.dt_to_iso_str)
    TIME = JobColumn('Execution Time', lambda job: job.execution_time, util.format_timedelta)
    STATE = JobColumn('State', lambda job: job.state, lambda state: state.name)
    WARNINGS = JobColumn('Warnings', lambda job: job.warnings, _print_dict)
    STATUS = JobColumn('Status', lambda job: job.status)


def _init_table(columns):
    table = Table(box=box.SIMPLE)
    for column in columns:
        table.add_column(column.name)
    table.columns[-1].justify = 'full'
    return table


class JobInstancesView:

    def __init__(self, columns, model):
        self._columns = columns
        self._model = model
        self._status_panel = StatusPanel(model)
        self._table = _init_table(columns)
        self._spinner = Spinner('simpleDotsScrolling', "[bold green]Fetching jobs...")
        self._hosts_completed = 0

    def _sync_rows(self):
        new_jobs = self._model.job_instances[len(self._table.rows):]
        for job in new_jobs:
            self._table.add_row(*(c.val_to_render(c.job_to_column_val(job)) for c in self._columns))

    def __rich__(self):
        self._sync_rows()

        renders = [self._status_panel]
        if len(self._table.rows) > 0:
            renders.append(self._table)
        if not self._model.is_completed():
            renders.append(self._spinner)

        return Group(*renders)


class StatusPanel:

    def __init__(self, model):
        self._grid = Table.grid(expand=True)
        self._grid.add_column(ratio=1)
        self._grid.add_column(ratio=1)
        self._grid.add_row(HostsPanel(model), JobsPanel(model))

    def __rich__(self):
        return self._grid


class HostsPanel:

    def __init__(self, model):
        self._model = model
        self._progress_bar = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.status]{task.completed}/{task.total}",
            TimeElapsedColumn()
        )
        self._task_id = self._progress_bar.add_task('[#ffc107]Hosts[/]', total=model.host_count)

        grid = Table.grid()
        grid.add_row(
            Padding(self._progress_bar, (0, 3, 0, 0)),
            SingleValue('Successful', lambda: model.host_successful_count, 4),
            SingleValue('Failed', lambda: len(model.host_to_error), 4),
        )
        self._panel = Panel(grid, title="[#009688]Hosts[/]", style='#009688')

    def _sync_progress(self):
        new_completed = self._model.host_completed_count - self._find_task().completed
        self._progress_bar.update(self._task_id, advance=new_completed)

    def _find_task(self):
        return next(task for task in self._progress_bar.tasks if task.id == self._task_id)

    def __rich__(self):
        self._sync_progress()
        return self._panel


class JobsPanel:

    def __init__(self, model):
        self._model = model

        grid = Table.grid()
        grid.add_row(
            SingleValue('Instances', lambda: len(model.job_instances), 4),
            SingleValue('Warning', lambda: len(model.job_instances.warning_instances()), 4)
        )

        self.panel = Panel(grid, title="[#009688]Jobs[/]", style='#009688')

    def __rich__(self):
        return self.panel


class SingleValue:

    def __init__(self, name, value, right_padding):
        self.name = name
        self.value = value
        self.right_padding = right_padding

    def __rich__(self):
        return Text(f"{self.name}: {self.value():<{self.right_padding}}", style="#ffc107")
