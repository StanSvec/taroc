from taroc import JobInstances


def test_slicing():
    sut = JobInstances([1, 2, 3])
    assert [2, 3] == list(sut[1:])
