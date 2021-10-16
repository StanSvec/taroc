import textwrap
from pathlib import Path

from taroc import JobInstance
from taroc.job import ExecutionState

J1_1 = JobInstance('h1', 'j1', 'i1_1', {}, ExecutionState.NONE, None, None, None, None, None, None, {}, None)
J1_2 = JobInstance('h1', 'j1', 'i1_2', {}, ExecutionState.NONE, None, None, None, None, None, None, {}, None)
J2_1 = JobInstance('h1', 'j2', 'i2_1', {}, ExecutionState.NONE, None, None, None, None, None, None, {}, None)


def create_test_file(file, content):
    with open(file, 'w') as outfile:
        outfile.write(textwrap.dedent(content))


def remove_test_file(file):
    host_file = Path(file)
    if host_file.exists():
        host_file.unlink()