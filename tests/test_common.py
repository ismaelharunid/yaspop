#!/usr/bin/env python

"""Tests for `yaspop` package."""

import pytest


from yaspop import common


def test_isnseq():
  """Test submodule common's isnseq."""
  assert common.isnseq([], 0)
  assert common.isnseq([None], 1)
  assert common.isnseq([1,2], 2)
  assert common.isnseq([], 0, list)
  assert common.isnseq([None], 1, list)
  assert common.isnseq([1,2], 2, list)


def test_isnmseq():
  """Test submodule common's isnmseq."""
  assert common.isnmseq((), 0)
  assert common.isnmseq((None,), 1)
  assert common.isnmseq((1,2), 2)
  assert common.isnmseq((), 0, 2)
  assert common.isnmseq((None,), 1, 2)
  assert common.isnmseq((1,2), 2, 3)


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


def test_isnmtuple():
  """Test submodule common's isnmtuple."""
  assert common.isnmtuple((), 0)
  assert common.isnmtuple((None,), 1)
  assert common.isnmtuple((1,2), 2)
  assert common.isnmtuple((), 0, 2)
  assert common.isnmtuple((None,), 1, 2)
  assert common.isnmtuple((1,2), 2, 3)


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


def test_reverse_partial():
  """Test submodule common's reverse_partial."""
  assert common.reverse_partial(abs, -4)() == 4


def test_dbg_print():
  """Test submodule common's dbg_print."""
  assert common.dbg_print('hello') is None
  
