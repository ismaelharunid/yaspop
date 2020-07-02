
from .common import Mapping, Sequence, RequiredValue \
    , dbg_print
import warnings


CONFIG_VALUE_TYPES = (bool, int, float, str \
    , type(RequiredValue), type(None))



class Setting(property):
  
  # class properties
  _tag      = 'abstract'
  _cast     = None
  
  @property
  def tag(cls):
    return self._tag
  
  @classmethod
  def Factory(cls, clsname, cast
      , bases=None, mixins=None, tag=None):
    if not isinstance(clsname, str):
      raise ValueError("clsname must be a non-empty string")
    if not callable(cast):
      raise ValueError("cast must be callable but is {:s}")
    if bases is None:
      bases = ()
    elif not isinstance(bases, Sequence) \
        or any(not isinstance(b, type) for b in bases):
      raise ValueError("bases must be a Sequence of classes or types")
    if mixins is None:
      mixins = {}
    elif not isinstance(mixins, Mapping):
      raise ValueError("mixins must be a Mapping of attributes")
    if tag is None:
      tag = clsname
    pcast = property(lambda s: tag, doc="cast {:s} to {:s}" \
        .format(tag, cast.__name__))
    return type(clsname, (Setting, *bases,)
        , {"cast": pcast, "tag": ptag, **mixins})
  
  def __new__(cls, name, default=None
      , getter=True, setter=None, deleter=None, doc=None
      ):
    self = super().__new__(cls)
    self._name = name
    return self
  
  # instance properties
  _default  = None
  
  @property
  def default(self):
    return self._default
  
  def __init__(self, name, default=None
      , getter=True, setter=None, deleter=None, doc="Undocumented"):
    dbg_print("Setting.__init__", name, default
        , getter, setter, deleter, doc)
    cast = self._cast
    value = None if default in (RequiredValue, None) else \
        cast(default)
    setter_wrapper = None
    if getter is True:
      if callable(setter):
        raise AttributeError("if {:s} getter is True then the".format(name) \
            + " setter may only be True or False (or None defaulting to True")
      if default is RequiredValue:
        if setter is False:
          raise AttributeError("if {:s} getter is True and".format(name) \
            + " default is RequiredValue then the setter may only be True" \
            + " (or None defaulting to True")
        if deleter:
          raise AttributeError("if {:s} getter is True and".format(name) \
            + " default is RequiredValue then deleters are not allowed")
      getter = lambda self: value
      if setter is True or default is RequiredValue:
        def setter_wrapper(self, val):
          nonlocal value, default
          if val is None:
            if default is RequiredValue:
              raise AttributeError("{:s} is a required value".format(name))
            val = None if default is None else cast(default)
          value = val
    elif setter is True:
      raise AttributeError("if {:s} getter is not True then the setter" \
      + " may only be callable or None".format(name))
    elif not setter and default is RequiredValue:
      raise AttributeError("if {:s} getter is not True and".format(name) \
          + " default is RequiredValue then the setter may only be callable")
    elif callable(setter):
      def setter_wrapper(self, val):
        nonlocal default, setter
        if val is None:
          if default is RequiredValue:
            raise AttributeError("{:s} is a required value".format(name))
          setter(self, None if default is None else cast(default))
    dbg_print("Setting.__init__ (before super)", name, default
      , getter, setter, deleter, doc)
    self._default = default
    super().__init__(getter, setter_wrapper, deleter, doc)
    dbg_print("Setting.__init__ (after super)", name, default
      , getter, setter, deleter, doc)
  
  def __bool__(self):
    return bool(self.default if self is None else self)
  
  def __float__(self):
    return float(self.default if self is None else self)
  
  def __int__(self):
    return int(self.default if self is None else self)
  
  def __str__(self):
    return str(self.default if self is None else self)
  
Setting.__index__ = Setting.__int__


class SettingMap(Mapping):
  
  @classmethod
  def Factory(cls, name, settings, base=None, repr_=None):
    # settings is (Setting instance, *setting_args)
    def __init__(self, initializer={}):
      for key in self._keys:
        self._settings[key] = settings[key](initializer[key] if key in initializer else None)
    def __getitem__(self, key):
      if key in self._keys:
        self._settings[key].value
      raise KeyError("invalid key {:s}".format(key))
    def __setitem__(self, key, value):
      if key in self._keys:
        self._settings[key].value = value
      raise KeyError("invalid key {:s}".format(key))
    bases = (cls,) if base is None else (cls, base)
    mixins = {"_settings": settings}
    return type(name, bases, mixins)
