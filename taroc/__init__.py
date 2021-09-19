from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional

from taroc import cfgfile, paths, cfg, sshclient


def load_defaults(**kwargs):
    cfgfile.load_default()
    setup(**kwargs)


def load_config(config=None, **kwargs):
    cfgfile.load(config)
    setup(**kwargs)


def setup(**kwargs):
    cfg.set_variables(**kwargs)


class ExecutionStateGroup(Enum):
    BEFORE_EXECUTION = auto()
    EXECUTING = auto()
    TERMINAL = auto()
    NOT_COMPLETED = auto()
    NOT_EXECUTED = auto()
    FAILURE = auto()


class ExecutionState(Enum):
    NONE = {}
    CREATED = {ExecutionStateGroup.BEFORE_EXECUTION}
    PENDING = {ExecutionStateGroup.BEFORE_EXECUTION}
    WAITING = {ExecutionStateGroup.BEFORE_EXECUTION}

    RUNNING = {ExecutionStateGroup.EXECUTING}

    COMPLETED = {ExecutionStateGroup.TERMINAL}
    STOPPED = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.NOT_COMPLETED}
    INTERRUPTED = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.NOT_COMPLETED}
    DISABLED = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.NOT_EXECUTED}
    CANCELLED = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.NOT_EXECUTED}
    SKIPPED = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.NOT_EXECUTED}

    FAILED = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.FAILURE}
    ERROR = {ExecutionStateGroup.TERMINAL, ExecutionStateGroup.FAILURE}


@dataclass(frozen=True)
class ExecutionError:
    message: str


@dataclass(frozen=True)
class JobInstance:
    job_id: str
    instance_id: str
    state_changes: dict[ExecutionState, datetime]
    status: Optional[str]
    warnings: dict[str, int]
    execution_error: Optional[ExecutionError]


def ps(*hosts):
    return sshclient.create_tasks('ps -f json', *hosts)
