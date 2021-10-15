from abc import ABC, abstractmethod
from datetime import timedelta, datetime

from rich import box
from rich.console import Group, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import Progress, BarColumn, ProgressColumn, Task
from rich.spinner import Spinner
from rich.table import Table, Column
from rich.text import Text

from taroc import JobInstance, util, theme
from taroc.job import ExecutionState
from tarocapp.model import JobInstancesModelObserver, JobInstancesModel, ModelUpdateEvent


class JobColumn(ABC):

    def __init__(self, header, none_placeholder=''):
        self.header = header
        self.none_renderable = none_placeholder
        self.column = Column(header=header)

    @abstractmethod
    def value(self, job_instance: JobInstance):
        """Return value for the column"""

    def renderable(self, job_instance) -> RenderableType:
        return self.job_to_str(job_instance)

    def job_to_str(self, job_instance):
        return self.value_to_str(self.value(job_instance))

    def value_to_str(self, value) -> RenderableType:
        if value is None:
            return self.none_renderable
        if isinstance(value, ExecutionState):
            return value.name
        if isinstance(value, datetime):
            return util.dt_to_iso_str(value)
        if isinstance(value, timedelta):
            return util.format_timedelta(value)
        if isinstance(value, dict):
            return _print_dict(value)

        return str(value)


class StaticJobColumn(JobColumn):

    def __init__(self, header, value_fnc, style='bright_white'):
        super().__init__(header)
        self.value_fnc = value_fnc
        self.style = style

    def value(self, job_instance: JobInstance):
        return self.value_fnc(job_instance)

    def renderable(self, job_instance):
        return Text(self.job_to_str(job_instance), style=self.style)


def _print_dict(dct):
    return ','.join(f"{k}:{v}" for k, v in dct)


class JobColumns:
    HOST = StaticJobColumn('Host', lambda job: job.host)
    JOB_ID = StaticJobColumn('Job ID', lambda job: job.job_id)
    INSTANCE_ID = StaticJobColumn('Instance ID', lambda job: job.instance_id)
    CREATED = StaticJobColumn('Created', lambda job: job.created)
    TIME = StaticJobColumn('Execution Time', lambda job: job.execution_time)
    STATE = StaticJobColumn('State', lambda job: job.state)
    WARNINGS = StaticJobColumn('Warnings', lambda job: job.warnings)
    STATUS = StaticJobColumn('Status', lambda job: job.status)


class JobInstancesView(JobInstancesModelObserver):

    def __init__(self, columns, model):
        self._columns = columns
        self._model = model
        self._status_panel = StatusPanel(model)
        self._table = Table(*[c.column for c in columns], box=box.SIMPLE)
        self._host_errors = HostErrors(model)
        self._spinner = Spinner('simpleDotsScrolling', f"[{theme.spinner}]Fetching jobs...", style=theme.spinner)

    def model_update(self, model: JobInstancesModel, event: ModelUpdateEvent):
        for job in event.new_instances:
            self._table.add_row(*(c.renderable(job) for c in self._columns))

    def __rich__(self):
        renders = [self._status_panel]
        if len(self._model.job_instances) > 0:
            renders.append(self._table)
        if len(self._model.host_errors) > 0:
            renders.append(self._host_errors)
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
            f"[{theme.progress_status}]" + "{task.completed}/{task.total}",
            CustomTimeElapsedColumn()
        )
        self._task_id = self._progress_bar.add_task(f"[{theme.hosts_panel_successful_name}]Connected[/]",
                                                    total=model.host_count)

        grid = Table.grid()
        grid.add_row(
            Padding(self._progress_bar, (0, 3, 0, 0)),
            HostsSuccessful('Successful', 4, model),
            HostsFailed('Failed', 4, model),
        )
        self._panel = Panel(grid, title=f"[{theme.hosts_panel_title}]Hosts[/]", style=theme.hosts_panel_border)

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
        grid.add_column()
        grid.add_column()
        grid.add_column(justify="right")
        grid.add_row(
            Instances('Instances', 4, model),
            WarningVal('Warning', 4, model),
            StateToCount(model),
        )

        self.panel = Panel(grid, title=f"[{theme.jobs_panel_title}]Jobs[/]", style=theme.jobs_panel_border)

    def __rich__(self):
        return self.panel


class SingleValue(ABC):

    def __init__(self, name, right_padding):
        self.name = name
        self.right_padding = right_padding

    @abstractmethod
    def value(self):
        """Return value to be displayed"""

    @abstractmethod
    def styles(self):
        """Return styles to be applied in form of ($name_style, $value_style)"""

    def __rich__(self):
        style_name, style_value = self.styles()

        t = Text()
        t.append(f"{self.name}: ", style=style_name)
        t.append(f"{self.value():<{self.right_padding}}", style=style_value)
        return t


class HostsSuccessful(SingleValue):

    def __init__(self, name, right_padding, model):
        super().__init__(name, right_padding)
        self.model = model

    def value(self):
        return self.model.host_successful_count

    def styles(self):
        return theme.hosts_panel_successful_name, theme.hosts_panel_successful_value


class HostsFailed(SingleValue):

    def __init__(self, name, right_padding, model):
        super().__init__(name, right_padding)
        self.model = model

    def value(self):
        return len(self.model.host_errors)

    def styles(self):
        return theme.hosts_panel_failed(self.value())


class Instances(SingleValue):

    def __init__(self, name, right_padding, model):
        super().__init__(name, right_padding)
        self.model = model

    def value(self):
        return len(self.model.job_instances)

    def styles(self):
        return theme.jobs_panel_instances_name, theme.jobs_panel_instances_value


class WarningVal(SingleValue):

    def __init__(self, name, right_padding, model):
        super().__init__(name, right_padding)
        self.model = model

    def value(self):
        return len(self.model.job_instances.warning_instances())

    def styles(self):
        return theme.jobs_panel_warning(self.value())


class StateToCount:

    def __init__(self, model):
        self._model = model

    def __rich__(self):
        return " | ".join(
            f"[white]{state.name}: {len(jobs)}[/]" for state, jobs in
            self._model.job_instances.state_to_instances().items())


class HostErrors:

    def __init__(self, model):
        self._model = model
        self._table = Table.grid()

    def _sync_rows(self):
        new_host_errors = self._model.host_errors[len(self._table.rows):]
        for host, err in new_host_errors:
            self._table.add_row(f"{host}: [red]{type(err).__name__} {err}[/]")

    def __rich__(self):
        self._sync_rows()

        return self._table


class CustomTimeElapsedColumn(ProgressColumn):
    """Renders time elapsed."""

    def render(self, task: "Task") -> Text:
        """Show time remaining."""
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            return Text("-:--:--", style="white")
        delta = timedelta(seconds=int(elapsed))
        return Text(str(delta), style="white")
