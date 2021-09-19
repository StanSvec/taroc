from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Optional, Set

from taroc import util


class ExecutionStateGroup(Enum):
    BEFORE_EXECUTION = auto()
    EXECUTING = auto()
    TERMINAL = auto()
    NOT_COMPLETED = auto()
    NOT_EXECUTED = auto()
    FAILURE = auto()


class ExecutionState(Enum):

    @staticmethod
    def from_str(val):
        try:
            return ExecutionState[val.upper()]
        except KeyError:
            return ExecutionState.UNKNOWN

    NONE = {}
    UNKNOWN = {}
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

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, groups: Set[ExecutionStateGroup]):
        self.groups = groups

    def is_before_execution(self):
        return ExecutionStateGroup.BEFORE_EXECUTION in self.groups

    def is_executing(self):
        return ExecutionStateGroup.EXECUTING in self.groups

    def is_incomplete(self):
        return ExecutionStateGroup.NOT_COMPLETED in self.groups

    def is_unexecuted(self):
        return ExecutionStateGroup.NOT_EXECUTED in self.groups

    def is_terminal(self) -> bool:
        return ExecutionStateGroup.TERMINAL in self.groups

    def is_failure(self) -> bool:
        return ExecutionStateGroup.FAILURE in self.groups


@dataclass(frozen=True)
class ExecutionError:
    message: str


@dataclass(frozen=True)
class JobInstance:
    job_id: str
    instance_id: str
    state_changes: dict[ExecutionState, datetime]
    state: ExecutionState
    created: Optional[datetime]
    last_changed: Optional[datetime]
    execution_started: Optional[datetime]
    execution_finished: Optional[datetime]
    execution_time: Optional[timedelta]
    status: Optional[str]
    warnings: dict[str, int]
    execution_error: Optional[ExecutionError]


def dto_to_job_instance(dct):
    exec_error = ExecutionError(dct['exec_error']) if dct['exec_error'] is not None else None
    JobInstance(dct['job_id'],
                dct['instance_id'],
                _dto_to_state_changes(dct),
                ExecutionState.from_str(dct['state']),
                util.dt_from_utc_str(dct['created']),
                util.dt_from_utc_str(dct['last_changed']),
                util.dt_from_utc_str(dct['execution_started']),
                util.dt_from_utc_str(dct['execution_finished']),
                timedelta(seconds=dct['execution_time']) if dct.get('execution_time') is not None else None,
                dct['status'],
                dct['warnings'],
                exec_error)


def _dto_to_state_changes(dct):
    return {ExecutionState.from_str(state_change['state']): util.dt_from_utc_str(state_change['changed'])
            for state_change in dct['lifecycle']['state_changes']}
