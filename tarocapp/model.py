from taroc import JobInstances


class JobInstancesModel:

    def __init__(self, host_count):
        self._host_count = host_count
        self._host_completed_count = 0
        self._job_instances = JobInstances()

    @property
    def host_count(self):
        return self._host_count

    @property
    def host_completed_count(self):
        return self._host_completed_count

    @property
    def job_instances(self):
        return JobInstances(self._job_instances)

    def add_host_jobs(self, host, jobs):
        self._host_completed_count += 1
        self._job_instances += jobs

    def is_completed(self):
        return self._host_count == self._host_completed_count
