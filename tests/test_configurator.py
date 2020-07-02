#!/usr/bin/env python

"""Tests for `yaspop` package."""

import pytest


from yaspop.configurator import Setting, RequiredValue, Configuration


def test_SettingFactory_bool():
  """Test submodule configurator's Setting.Factory."""
  BoolSetting = Setting.Factory("test", "tag", bool)
  i = BoolSetting("test_bool", None)
  assert i.value is None
  i.value = 1
  assert i.value == True
  assert type(i.value) is bool
  i.value = "2"
  assert i.value == True
  assert type(i.value) is bool
  i.value = 3.
  assert i.value == True 
  assert type(i.value) is bool

def test_SettingFactory_required_bool():
  """Test submodule configurator's Setting.Factory."""
  BoolSetting = Setting.Factory("test", "tag", bool, defval=RequiredValue)
  try:
    i = BoolSetting("test_bool", None)
    assert False
  except:
    pass
  i = BoolSetting("test_bool", False)
  i.value = 1
  assert i.value == True
  assert type(i.value) is bool
  i.value = "2"
  assert i.value == True
  assert type(i.value) is bool
  i.value = 3.
  assert i.value == True 
  assert type(i.value) is bool

def test_SettingFactory_default_bool():
  """Test submodule configurator's Setting.Factory."""
  BoolSetting = Setting.Factory("test", "tag", bool, defval=False)
  i = BoolSetting("test_bool", None)
  assert i.value == False
  assert type(i.value) is bool
  i.value = 1
  assert i.value == True
  assert type(i.value) is bool
  i.value = "2"
  assert i.value == True
  assert type(i.value) is bool
  i.value = 3.
  assert i.value == True 
  assert type(i.value) is bool

def test_SettingFactory_int():
  """Test submodule configurator's Setting.Factory."""
  IntSetting = Setting.Factory("test", "tag", int)
  i = IntSetting("test_int", None)
  assert i.value is None
  i.value = 1
  assert i.value == 1
  assert type(i.value) is int
  i.value = "2"
  assert i.value == 2
  assert type(i.value) is int
  i.value = 3.
  assert i.value == 3 
  assert type(i.value) is int

def test_SettingFactory_float():
  """Test submodule configurator's vreateConfiguration."""
  IntSetting = Setting.Factory("test", "tag", float)
  i = IntSetting("test_float", None)
  assert i.value is None
  i.value = 1
  assert i.value == 1
  assert type(i.value) is float
  i.value = "2"
  assert i.value == 2
  assert type(i.value) is float
  i.value = 3.
  assert i.value == 3 
  assert type(i.value) is float

def test_SettingFactory_str():
  """Test submodule configurator's vreateConfiguration."""
  IntSetting = Setting.Factory("test", "tag", str)
  i = IntSetting("test_str", None)
  assert i.value is None
  i.value = 1
  assert i.value == "1"
  assert type(i.value) is str
  i.value = "2"
  assert i.value == "2"
  assert type(i.value) is str
  i.value = 3.
  assert i.value == "3.0" 
  assert type(i.value) is str