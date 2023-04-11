# Python 3 compatibility helpers

import inspect
import sys

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

try:
    buffer = buffer
except NameError:
    buffer = memoryview

try:
    long = long
except NameError:
    long = int

try:
    unicode = unicode
except NameError:
    unicode = str

try:
    basestring = basestring
except NameError:
    basestring = (bytes, str)

def cmp(a, b):
    return (a > b) - (a < b)

_convert = {
    '__eq__': lambda self, other: self.__cmp__(other) == 0,
    '__ne__': lambda self, other: self.__cmp__(other) != 0,
    '__lt__': lambda self, other: self.__cmp__(other) < 0,
    '__le__': lambda self, other: self.__cmp__(other) <= 0,
    '__gt__': lambda self, other: self.__cmp__(other) > 0,
    '__ge__': lambda self, other: self.__cmp__(other) >= 0,
}

def PY3__cmp__(cls):
    """Class decorator that fills in missing ordering methods when Python2's __cmp__ is provided."""
    if not hasattr(cls, '__cmp__'):
        raise ValueError('must define the __cmp__ Python2 operation')
    if sys.version_info < (3, 0, 0):
        return cls
    for op, opfunc in _convert.items():
        # Overwrite `raise NotImplemented` comparisons inherited from object
        if getattr(cls, op, None) is getattr(object, op, None):
            setattr(cls, op, opfunc)
    return cls

if hasattr(inspect, 'formatargspec'):
    formatargspec = inspect.formatargspec
else:
    def formatargspec(args, varargs, keywords, defaults, formatvalue=str):
        params = []
        for arg in args:
            params.append(inspect.Parameter(arg, inspect.Parameter.POSITIONAL_OR_KEYWORD))
        if defaults:
            for i, d in enumerate(reversed(defaults)):
                idx = len(params) - 1 - i
                params[idx] = params[idx].replace(default=d)
        if varargs:
            params.append(inspect.Parameter(varargs, inspect.Parameter.VAR_POSITIONAL))
        if keywords:
            params.append(inspect.Parameter(keywords, inspect.Parameter.VAR_KEYWORD))

        return str(inspect.Signature(params))
