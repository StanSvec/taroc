from taroc import JobInstances
from tarocapp.model import JobInstancesModel
from test.util import *


def test_add_jobs_update():
    # Given
    observed = 0

    def model_update(model, event):
        # Then:
        assert sut == model
        assert JobInstances([J1_2, J2_1]) == event.new_instances
        nonlocal observed
        observed += 1

    any_ = 3
    sut = JobInstancesModel(any_)
    sut.add_host_jobs('any', [J1_1])
    sut.observers.append(model_update)

    # When:
    sut.add_host_jobs('any', [J1_2, J2_1])

    # Then:
    assert observed == 1


def test_add_error_update():
    observed = 0

    def model_update(_, event):
        assert len(event.new_instances) == 0
        nonlocal observed
        observed += 1

    sut = JobInstancesModel(1)
    sut.observers.append(model_update)

    sut.add_host_error('any', None)

    assert observed == 1
