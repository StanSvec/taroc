import abc
from dataclasses import dataclass

from taroc import JobInstances


def updates(func):
    def notify_observers(model, *args, **kwargs):
        cur_instances = model.job_instances
        res = func(model, *args, **kwargs)
        new_instances = [job for job in model.job_instances if job not in cur_instances]
        model.notify_observers(ModelUpdateEvent(JobInstances(new_instances)))
        return res

    return notify_observers


class JobInstancesModel:

    def __init__(self, host_count):
        self.observers = []
        self._host_count = host_count
        self._host_successful_count = 0
        self._job_instances = JobInstances()
        self._host_error = []

    def notify_observers(self, event):
        for observer in self.observers:
            if callable(observer):
                observer(self, event)
            else:
                observer.model_update(self, event)

    @property
    def host_count(self) -> int:
        return self._host_count

    @property
    def host_successful_count(self) -> int:
        return self._host_successful_count

    @property
    def host_completed_count(self) -> int:
        return self._host_successful_count + len(self._host_error)

    @property
    def host_errors(self):
        return list(self._host_error)

    @property
    def job_instances(self) -> JobInstances:
        return JobInstances(self._job_instances)

    @updates
    def add_host_jobs(self, host, jobs):
        self._host_successful_count += 1
        self._job_instances += jobs

    @updates
    def add_host_error(self, host, error):
        self._host_error.append((host, error))

    def is_completed(self):
        return self._host_count == self.host_completed_count


@dataclass
class ModelUpdateEvent:
    new_instances: JobInstances


class ExecutionStateObserver(abc.ABC):

    @abc.abstractmethod
    def model_update(self, model: JobInstancesModel, event: ModelUpdateEvent):
        """This method is called when job instance execution state is changed."""
