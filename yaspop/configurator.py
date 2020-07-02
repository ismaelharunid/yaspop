
from .common import Iterable, Mapping, Sequence \
    , Complex, Integral, Number, Rational, Real \
    , hasws, stripsplit, uniques \
    , reduce, dbg_print
import warnings


RequiredValue = type("RequiredValueType", (object,), {})()

CONFIG_VALUE_TYPES = (bool, int, float, str \
    , type(RequiredValue), type(None))



class Setting(object):
  
  @classmethod
  def Factory(cls, name, tag, cast, defval=None, base=None, repr_=None):
    if repr_ is None:
      repr_ = cast.__repr__
    bases = (cls,) if base is None else (cls, base)
    defval, required = (None, True) if defval is RequiredValue else \
        (defval, False)
    mixins = \
        { "Tag": property(lambda s: tag, None, None, "setting tag")
        , "cast": property(lambda s: cast, None, None, "setting type")
        , "defval": property(lambda s: defval, None, None, "default value")
        , "required": property(lambda s: required, None, None, "required value")
        , "__repr__": repr_
        }
    return type(name, bases, mixins)
  
  _name     = None
  _value    = None
  
  @property
  def Tag(self):
    raise NotImplementedError("Tag on abstract class go figure.")
  
  @property
  def cast(self):
    raise NotImplementedError("cast on abstract class go figure.")
  
  @property
  def defval(self):
    raise NotImplementedError("name on abstract class go figure.")
  
  @property
  def required(self):
    raise NotImplementedError("required on abstract class go figure.")
  
  @property
  def name(self):
    return self._name
  
  @property
  def value(self):
    return self._value
  
  @value.setter
  def value(self, value):
    if value is None:
      if self.required:
        raise ValueError("{:s} requires an {:s} value" \
            .format(self._name, self.cast.__name__))
      value = self.defval
    self._value = None if value is None else self.cast(value)
  
  def __init__(self, name, value):
    self._name    = name
    self.value    = value
  
  def __bool__(self):
    return bool(self.defval if self._value is None else self._value)
  
  def __float__(self):
    return float(self.defval if self._value is None else self._value)
  
  def __int__(self):
    return int(self.defval if self._value is None else self._value)
  
  def __str__(self):
    return str(self.defval if self._value is None else self._value)

Setting.__index__ = Setting.__int__


class Configuration(Mapping):
  
  _settings     = None
  
  def __init__(self):
    pass


