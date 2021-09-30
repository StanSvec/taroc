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
    host: str
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


class JobInstances(list):

    def __init__(self, *jobs):
        list.__init__(self, *jobs)

    def __add__(self, jobs):
        return JobInstances(list.__add__(self, jobs))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return JobInstances(result)
        except TypeError:
            return result

    def warning_instances(self):
        return [job for job in self if job.warnings]


def dto_to_job_instance(host, dct) -> JobInstance:
    lc = dct['lifecycle']
    exec_error = ExecutionError(dct['exec_error']) if dct['exec_error'] is not None else None
    return JobInstance(host,
                       dct['job_id'],
                       dct['instance_id'],
                       _dto_to_state_changes(lc),
                       ExecutionState.from_str(lc['state']),
                       util.dt_from_utc_str(lc['created']),
                       util.dt_from_utc_str(lc['last_changed']),
                       util.dt_from_utc_str(lc['execution_started']),
                       util.dt_from_utc_str(lc['execution_finished']),
                       timedelta(seconds=lc['execution_time']) if lc.get('execution_time') is not None else None,
                       dct['status'],
                       dct['warnings'],
                       exec_error)


def dto_to_job_instances(host, dct) -> JobInstances:
    return JobInstances([dto_to_job_instance(host, job_dct) for job_dct in dct['jobs']])


def _dto_to_state_changes(lifecycle):
    return {ExecutionState.from_str(state_change['state']): util.dt_from_utc_str(state_change['changed'])
            for state_change in lifecycle['state_changes']}
