# -*- coding: utf-8 -*-
from inspect import isclass
from collections import MutableMapping


__all__ = ("isclass", "isdict", "istuple", "isstring")


def validator(func):
    def wrapper(*args, strict=False, **kwargs):
        result = func(*args, **kwargs)
        if strict:
            assert result, \
                "validation error" \
                "\n\tValidator: %s" \
                "\n\targs: %s" \
                "\n\tkwargs: %s" \
                % (repr(func), repr(args), repr(kwargs))
        return result
    return wrapper


@validator
def isdict(value):
    return isinstance(value, MutableMapping)


@validator
def istuple(value):
    return isinstance(value, tuple)


@validator
def isstring(value):
    return isinstance(value, str)
