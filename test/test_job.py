from taroc import JobInstances
from test.util import *


def test_slicing():
    sut = JobInstances([J1_1, J1_2, J2_1])
    assert [J1_2, J2_1] == list(sut[1:])
