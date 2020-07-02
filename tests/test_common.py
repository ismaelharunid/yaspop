#!/usr/bin/env python

"""Tests for `yaspop` package."""

import pytest

from yaspop import common

def text_constants():
  """Test submodule common's constants."""
  assert type(None) is common.NoneType
  assert common.RequiredValue \
      and type(common.RequiredValue) is common.RequiredValueType

def test_required():
  """Test submodule common's required functions."""
  assert common.isrequired(common.RequiredValue)
  assert not common.isrequired(None)
  assert common.withdefault(None) is None
  assert common.withdefault(1) == 1
  assert common.withdefault(None, None) is None
  assert common.withdefault(1, None) == 1
  assert common.withdefault(None, 1) == 1
  assert common.withdefault(1, 1) == 1
  assert common.withdefault(1, types=int) == 1
  
  #assert withdefault(None, 1, types=None, name="obj") == 1

def test_izzy_functions():
  """Test submodule common's izzy functions."""
  assert common.isbool(bool(1))
  assert common.isfloat(float(1))
  assert common.isint(int(1))
  assert common.isstr(str(1))
  assert common.isnumeric(False)
  assert common.isnumeric(True)
  assert common.isnumeric(0)
  assert common.isnumeric(1)
  assert common.isnumeric(2.0)
  assert not common.isnumeric("2.0")


def test_isnseq():
  """Test submodule common's isnseq."""
  assert common.isnseq([], 0)
  assert common.isnseq([None], 1)
  assert common.isnseq([1,2], 2)
  assert common.isnseq([], 0, c=list)
  assert common.isnseq([None], 1, c=list)
  assert common.isnseq([1,2], 2, c=list)


def test_isnmseq():
  """Test submodule common's isnmseq."""
  assert common.isnmoseq((), 0)
  assert common.isnmoseq((None,), 1)
  assert common.isnmoseq((1,2), 2)
  assert common.isnmoseq((), 0, 2)
  assert common.isnmoseq((None,), 1, 2)
  assert common.isnmoseq((1,2), 2, 3)


def test_is2tuple():
  """Test submodule common's is2tuple."""
  assert common.is2tuple((None,None))
  assert common.is2tuple((None,1))
  assert common.is2tuple((0,None))
  assert common.is2tuple((1,2))
  assert common.is2tuple((0.5,1.0))
  assert common.is2tuple(("a","b"))


def test_isntuple():
  """Test submodule common's isntuple."""
  assert common.isntuple((), 0)
  assert common.isntuple((None,), 1)
  assert common.isntuple((1,2), 2)
  assert common.isntuple((), 0)
  assert common.isntuple((None,), 1)
  assert common.isntuple((1,2), 2)


def test_hasws():
  """Test submodule common's hasws."""
  assert common.hasws("all the time")
  assert common.hasws(" ")
  assert common.hasws("\n")
  assert not common.hasws("")


def test_stripsplit():
  """Test submodule common's stripsplit."""
  assert tuple(common.stripsplit("all the time")) == ("all", "the", "time")
  assert tuple(common.stripsplit("")) == ()
  assert tuple(common.stripsplit("   ")) == ()
  assert tuple(common.stripsplit(" many   differnt   things ")) == ("many", "differnt", "things")
  assert tuple(common.stripsplit(",,,,", ",")) == ()
  assert tuple(common.stripsplit("one, two, three", ",")) == ("one", "two", "three")
  assert tuple(common.stripsplit("one, two, three", ",", 1)) == ("one", "two, three")
  assert tuple(common.stripsplit("==one==, ==two==, three  ,=four===", ",", 2, '= ')) == ('one', 'two', 'three  ,=four')


def test_uniques():
  """Test submodule common's uniques."""
  assert common.uniques((1,2,3), (2,3,4), (3,4,5) * 10) == (1,2,3,4,5)
  assert common.uniques(tuple(range(20)), range(10,30), target=[]) == list(range(30))
  assert common.uniques((1,2,3), (2,2,3,4,4,4), (3,4,5,3,4,5,3,4,5), ()) == (1, 2, 3, 4, 5)
  assert common.uniques((1,2,3), (2,2,3,4,4,4), (3,4,5,3,4,5,3,4,5), (), target=[]) == [1, 2, 3, 4, 5]


def test_bind():
  """Test submodule common's bind."""
  assert common.bind(max, (-4,), (4,))() == 4
  assert common.bind(min, (-4,), (4,))() == -4


def test_dbg_print():
  """Test submodule common's dbg_print."""
  assert common.dbg_print('hello') is None


def test_classproperty():
  """Test classproperty decorator."""
  
  class Foo(object):
    @common.classproperty
    def z(cls):
      return "YES"
  
  f = Foo()
  assert Foo.z == "YES"
  assert f.z == "YES"
