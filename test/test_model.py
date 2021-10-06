from taroc import JobInstances
from tarocapp.model import JobInstancesModel
from test.util import *


def test_observing():
    # Given
    observed = 0

    def model_update(model, event):
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

    assert observed == 1
