from taroc import JobInstances


class JobInstancesModel:

    def __init__(self, host_count):
        self._host_count = host_count
        self._host_successful_count = 0
        self._job_instances = JobInstances()
        self._host_error = []

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

    def add_host_jobs(self, host, jobs):
        self._host_successful_count += 1
        self._job_instances += jobs

    def add_host_error(self, host, error):
        self._host_error.append((host, error))

    def is_completed(self):
        return self._host_count == self.host_completed_count
