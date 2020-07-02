
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
try:
  from collections.abc import Iterable, Mapping, Sequence
except ImportError:
  from collections import  Iterable, Mapping, Sequence

from numbers import Complex, Integral, Number, Rational, Real
from functools import reduce, partial

toseq = lambda obj, t=tuple: obj if isnseq(obj) else t((pbj,))

NoneType = type(None)
RequiredValueType = type("RequiredValueType", (object,), {})
RequiredValue = RequiredValueType()

isrequired = lambda obj: obj is RequiredValue

def withdefault(obj, default=None, types=None, name="obj"):
  if obj is None:
    if isrequired(default):
      raise ValueError("{:s} is required".format(name))
    obj = default
  if types is not None and not isinstance(obj, types):
    raise ValueError("{:s} expects {:s} but found {:s}" \
        .format(name
        , wordjoin(types, repr=lambda i: type(i).__name__)
        , repr(obj)))
  return obj

isbool = lambda obj: type(obj) is bool
isfloat = lambda obj: type(obj) is float
isint = lambda obj: type(obj) is int
isstr = lambda obj: type(obj) is str
isnumeric = lambda obj: isinstance(obj, Number)
isiterable = lambda obj: isinstance(obj, Iterable)

is2tuple = lambda obj, i=None: isnseq(obj, 2, c=tuple, i=i)
isntuple = lambda obj, n, i=None: isnseq(obj, n, c=tuple, i=i)
isnseq = lambda obj, n=0, c=Sequence, i=None: isnmoseq(obj, n, n, c, i)
isnmoseq = lambda obj, n=0, m=None, c=Sequence, i=None: \
    (c is None or isinstance(obj, c)) \
    and n <= len(obj) and (m is None or len(obj) <= m) \
    and (i is None or all(isinstance(i, i) for i in obj))

hasws   = lambda txt: isstr(txt) and any(c.isspace() for c in txt)

stripsplit = lambda txt, sep=None, maxsplit=-1, chars=None: \
    (t.strip(chars) for t in txt.split(sep, maxsplit) if t.strip(chars))

wordjoin = lambda seq, sep=', ', lastsep=' or ', repr=repr: \
    sep.join(repr(i) for i in seq[:-1]) \
    + (sep if lastsep is None else lastsep) + repr(seq[-1])

def uniques(*sources, target=None):
  ttype = type(sources[0] if target is None else target)
  if target is None:
    target = ttype(())
  for source in sources:
    target = reduce((lambda a,c: a if c in a else a+ttype((c,))) \
        , source, target)
  return target

def bind(func, pre=(), post=(), kwpre={}, kwpost={}):
  return lambda *args, **kwargs: \
    func(*(*pre,*args,*post), **{**kwpre,**kwargs,**kwpost})


class classproperty(property):
  def __get__(self, obj, objtype=None):
    return super().__get__(objtype)
  def __set__(self, obj, value):
    super().__set__(type(obj), value)
  def __delete__(self, obj):
    super().__delete__(type(obj))


if "DEBUG" not in globals():
  DEBUG = 0

def dbg_print(*args, **kargs):
  if DEBUG:
    print("DGB:", *args, **kargs)
