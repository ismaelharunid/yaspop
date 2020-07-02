#!/usr/bin/env python

"""Tests for `yaspop` package."""


from yaspop.common import RequiredValue
from yaspop.settings import Setting


def test_settings():

    class Foo():

        _settings = {}

        def __init__(self, *args):
            if args:
                self.s = args[0]

        def tag(self, name):
            return self._settings[name]._tag

    s = Setting('test')
    Foo.s = s
    f = Foo()
    assert f.s is None
    try:
        f.s = 8
        assert False
    except AttributeError:
        pass

    s = Setting('test', RequiredValue)
    Foo.s = s
    try:
        f = Foo(None)
        assert False
    except AttributeError:
        pass

    s = Setting('test', RequiredValue, setter=True)
    Foo.s = s
    try:
        f = Foo(None)
        assert False
    except AttributeError:
        pass

    s = Setting('test', RequiredValue)
    Foo.s = s
    f = Foo(2)
    assert f.s == 2

    s = Setting('test', RequiredValue, setter=True)
    Foo.s = s
    f = Foo(3)
    assert f.s == 3

    assert bool(f.s) is True and isinstance(bool(f.s), bool)
    assert int(f.s) == 3 and isinstance(int(f.s), int)
    assert float(f.s) == 3.0 and isinstance(float(f.s), float)
    assert str(f.s) == "3" and isinstance(str(f.s), str)
    assert repr(f.s) == "3" and isinstance(repr(f.s), str)
