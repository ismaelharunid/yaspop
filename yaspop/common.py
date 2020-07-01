

from collections.abc import Iterable, Mapping, Sequence
from numbers import Complex, Integral, Number, Rational, Real
from functools import reduce, partial

isnseq = lambda obj, n, t=Sequence: isinstance(obj, t) and len(obj) == n
isnmseq = lambda obj, n=0, m=None, t=Sequence: isinstance(obj, t) \
    and n <= len(obj) and (m is None or len(obj) <= m)

is2tuple = lambda obj: isnseq(obj, 2, tuple)
isntuple = lambda obj, n: isnseq(obj, n, tuple)
isnmtuple = lambda obj, n=0, m=None: isnmseq(obj, n, m, tuple)

hasws   = lambda txt: any(c.isspace() for c in txt)
stripsplit = lambda txt, sep=None, maxsplit=-1, chars=None: \
    (t.strip(chars) for t in txt.split(sep, maxsplit) if t.strip(chars))

def uniques(*sources, target=None):
  ttype = type(sources[0] if target is None else target)
  if target is None:
    target = ttype(())
  for source in sources:
    target = reduce((lambda a,c: a if c in a else a+ttype((c,))) \
        , source, target)
  return target

def reverse_partial(func, *args, **kwargs):
  return lambda *fargs, **fkwargs: \
    func(*fargs, *args, **{**fkwargs, **kwargs})


if "DEBUG" not in globals():
  DEBUG = 0

def dbg_print(*args, **kargs):
  if DEBUG:
    print("DGB:", *args, **kargs)
