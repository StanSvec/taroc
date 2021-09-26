from dataclasses import dataclass
from typing import Callable, Any

from rich import box
from rich.columns import Columns
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
    val_to_render: Callable[[Any], RenderableType] = lambda val: str(val)


class JobColumns:
    HOST = JobColumn('Host', lambda job: job.host)
    JOB_ID = JobColumn('Job ID', lambda job: job.job_id)
    INSTANCE_ID = JobColumn('Instance ID', lambda job: job.instance_id)
    CREATED = JobColumn('Created', lambda job: job.created, util.dt_to_iso_str)
    TIME = JobColumn('Execution Time', lambda job: job.execution_time, util.format_timedelta)
    STATE = JobColumn('State', lambda job: job.state, lambda state: state.name)
    WARNINGS = JobColumn('Warnings', lambda job: job.warnings)
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
        self._model = model
        self._instance_count = SingleValue('Instances', lambda: len(model.job_instances), 5)
        self._progress_bar = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.status]{task.completed}/{task.total}",
            TimeElapsedColumn())
        self._task_id = self._progress_bar.add_task('[#ffc107]Hosts[/]', total=model.host_count)
        columns = Columns([Padding(self._progress_bar, (0, 3, 0, 0)),
                           self._instance_count,
                           Text(f"Total: {model.host_count}", style="#ffc107")])
        self.panel = Panel(columns, title="[#009688]Status[/]", style='#009688')

    def _sync_progress(self):
        task = next(task for task in self._progress_bar.tasks if task.id == self._task_id)
        new_completed = self._model.host_completed_count - task.completed
        self._progress_bar.update(self._task_id, advance=new_completed)

    def __rich__(self):
        self._sync_progress()

        return self.panel


class SingleValue:

    def __init__(self, name, value, right_padding):
        self.name = name
        self.value = value
        self.right_padding = right_padding

    def __rich__(self):
        return Text(f"{self.name}: {self.value():<{self.right_padding}}", style="#ffc107")
