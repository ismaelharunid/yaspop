
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
try:
    from collections.abc import Iterable, Mapping, Sequence
except ImportError:
    from collections import Iterable, Mapping, Sequence

from numbers import Number
from functools import reduce


def toseq(obj, t=tuple):
    """convert non-tuple values to a 1-tuple containing original value."""
    return obj if isnseq(obj) else t((obj,))


NoneType = type(None)
RequiredValueType = type("RequiredValueType", (object,), {})
RequiredValue = RequiredValueType()


def isrequired(obj):
    """Returns True if obj is RequiredValue, otherwise False."""
    return obj is RequiredValue


def withdefault(obj, default=None, types=None, name="obj"):
    """
    Return a default value if obj is None, otherwise the value.

    Return a default value if obj is None, otherwise the original value.
    Raises ValueError if default is isrequired, or if type(obj) is not
    in types and not None.

    Parameters:
    obj (any):  any original value
    default (any): any value, or None or RequiredValue
    types (type or (*types)): type constrains for obj
    name (str): optional tag for exceptions
    Returns:
    any:The original value or default if obj is None
    """
    if obj is None:
        if isrequired(default):
            raise ValueError("{:s} is required".format(name))
        obj = default
    if types is not None and not isinstance(obj, types):
        ztypes = wordjoin(types, repr=lambda i: type(i).__name__)
        raise ValueError("{:s} expects {:s} but found {:s}"
                        .format(name, ztypes, repr(obj)))
    return obj


def isbool(obj):
    """Returns True if type(obj) is bool, otherwise False."""
    return type(obj) is bool


def isfloat(obj):
    """Returns True if type(obj) is float, otherwise False."""
    return type(obj) is float


def isint(obj):
    """Returns True if type(obj) is int, otherwise False."""
    return type(obj) is int


def isstr(obj):
    """Returns True if type(obj) is str, otherwise False."""
    return type(obj) is str


def isnumeric(obj):
    """Returns True if obj is instance of Number, otherwise False."""
    return isinstance(obj, Number)


def isiterable(obj):
    """Returns True if obj is instance of Iterable, otherwise False."""
    return isinstance(obj, Iterable)


def isseq(obj):
    """Returns True if obj is instance of Sequence, otherwise False."""
    return isinstance(obj, Sequence)


def ismap(obj):
    """Returns True if obj is instance of Mapping, otherwise False."""
    return isinstance(obj, Mapping)


def is2tuple(obj, i=None):
    """Returns True if obj is a 2-tuple , otherwise False."""
    return isnseq(obj, 2, c=tuple, i=i)


def isntuple(obj, n, i=None):
    """Returns True if obj is a n-tuple , otherwise False."""
    return isnseq(obj, n, c=tuple, i=i)


def isnseq(obj, n=0, c=Sequence, i=None):
    """Returns True if obj is instance of Sequence, w/length n, else False."""
    return isnmoseq(obj, n, n, c, i)


def isnmoseq(obj, n=0, m=None, c=Sequence, i=None):
    """
    Returns True if obj is an (n..m)-c type with items of type i.

    If m is None then then length can be any greater than n.
    If i is None then the items may be of any type.
    Returns True if obj is instance of Sequence, with a length
    between n and m, and.  if m is None then length can
    anything more then n.  if i is not None, obj's items must be of
    type i; otherwise False is returned

    obj (any):  the subject to test.
    n (int):    the minimum length.
    m (int or None): the minimum length.
    c (type):   the container type obj must be.
    i (type):   the type obj's items must be.
    """
    return (c is None or isinstance(obj, c)) \
        and n <= len(obj) and (m is None or len(obj) <= m) \
        and (i is None or all(isinstance(i, i) for i in obj))


def hasws(txt):
    return isstr(txt) and any(c.isspace() for c in txt)


def stripsplit(txt, sep=None, maxsplit=-1, chars=None):
    return (t.strip(chars)
            for t in txt.split(sep, maxsplit)
            if t.strip(chars))


def wordjoin(seq, sep=', ', lastsep=' or ', repr=repr):
    return sep.join(repr(i) for i in seq[:-1]) \
            + (sep if lastsep is None else lastsep) \
            + repr(seq[-1])


def uniques(*sources, target=None):
    ttype = type(sources[0] if target is None else target)
    if target is None:
        target = ttype(())
    for source in sources:
        target = reduce((lambda a, c: a if c in a else a + ttype((c,))),
                        source, target)
    return target


def bind(func, pre=(), post=(), kwpre={}, kwpost={}):
    return lambda *args, **kwargs: \
        func(*(*pre, *args, *post), **{**kwpre, **kwargs, **kwpost})


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
