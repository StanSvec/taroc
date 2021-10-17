from taroc.ref import RefValue, ClassRefValueSupport


def test_access_def_value():
    class Test(metaclass=ClassRefValueSupport):
        f = RefValue(5)

    assert Test.f == 5
    assert Test().f == 5


def test_value_setting():
    class Test(metaclass=ClassRefValueSupport):
        f = RefValue(5)

    t1 = Test()
    t2 = Test()
    t2.f = 6

    assert t1.f == 5
    assert t2.f == 6

    Test.f = 4
    assert Test.f == 4
    assert t1.f == 4  # Static variable used as instance attribute not found
    assert t2.f == 6


def test_reference_def_val():
    class Test(metaclass=ClassRefValueSupport):
        f = RefValue(5)
        ref1 = RefValue(f)
        ref2 = RefValue(f)

    assert Test.ref1 == 5
    assert Test.ref2 == 5


def test_reference():
    class Test(metaclass=ClassRefValueSupport):
        f = RefValue(5)
        ref1 = RefValue(f)
        ref2 = RefValue(f)

    Test.f = 3
    assert Test.ref1 == 3
    assert Test.ref2 == 3


def test_reference_changes():
    class Test(metaclass=ClassRefValueSupport):
        f1 = RefValue(5)
        ref1 = RefValue(f1)
        ref2 = RefValue(f1)

    Test.f1 = 8
    Test.ref1 = 6
    assert Test.ref1 == 6
    assert Test.ref2 == 8
