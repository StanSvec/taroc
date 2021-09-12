from rich import box
from rich.columns import Columns
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.spinner import Spinner
from rich.table import Table


def _init_table(columns):
    table = Table(box=box.SIMPLE)
    for column in columns:
        table.add_column(column)
    table.columns[-1].justify = 'full'
    return table


class JobsView:

    def __init__(self, *, hosts_count, columns):
        self._status_panel = StatusPanel(hosts_count)
        self._table = _init_table(columns)
        self._spinner = Spinner('simpleDotsScrolling', "[bold green]Fetching jobs...")
        self._hosts_count = hosts_count
        self._hosts_completed = 0

    def add_host_rows(self, host, rows):
        self._hosts_completed += 1
        self._status_panel.completed()
        for row in rows:
            self._table.add_row(*row)

    def is_completed(self):
        return self._hosts_completed == self._hosts_count

    def __rich__(self):
        renders = [self._status_panel]
        if len(self._table.rows) > 0:
            renders.append(self._table)
        if not self.is_completed():
            renders.append(self._spinner)

        return Group(*renders)


class StatusPanel:

    def __init__(self, hosts_count):
        self.hosts_completed = SingleValue('Completed', 0)
        self.progress_bar = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.status]{task.completed}/{task.total}",
            TimeRemainingColumn())
        self.task = self.progress_bar.add_task('[#ffc107]Progress[/]', total=hosts_count)
        columns = Columns([self.progress_bar, self.hosts_completed, SingleValue('Total', hosts_count)])
        self.panel = Panel(columns, title="[#009688]Status[/]", style='#009688')

    def completed(self):
        self.progress_bar.update(self.task, advance=1)
        self.hosts_completed.value += 1

    def __rich__(self):
        return self.panel


class SingleValue:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __rich__(self):
        return Padding(f"{self.name}: {self.value}", (0, 5 - len(str(self.value)), 0, 5), style="#ffc107")
