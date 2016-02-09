# -*- coding: utf-8 -*-
from helpers import *
from functools import partial, partialmethod


class Proxy(object):

    def __init__(self, handler):
        self.handler = handler

    def __get__(self, instance, owner):
        subject = instance.subject
        handler = self.handler

        if callable(handler):
            method = partial(handler, instance, subject)
        elif isstring(handler):
            method = getattr(subject, handler)
        else:
            raise TypeError

        return method


class Facade(object):

    def __str__(self):
        return str(self.subject)

    def __repr__(self):
        return repr(self.subject)


def default_initializer(instance, subject, *args, **kwargs):
    instance.subject = subject(*args, **kwargs)


def make_adapter(subject, **adapted_methods):
    name = subject.__name__
    name = name.title()
    name += "Facade"
    bases = (Facade,)
    methods = {item: Proxy(handler)
               for item, handler in adapted_methods.items()}
    methods['__init__'] = partialmethod(default_initializer, subject)
    facade = type(name, bases, methods)
    return facade


def main():
    A = make_adapter(str, format_a="format")
    a = A("Hello {:s}")

    try:
        print(a.format_a("Jean"))
        print(a.format("Jean"))
    except AttributeError as e:
        print("HasAttr:", e)

    def format_handler(instance, subject, *args, **kwargs):
        result = subject.format(*args, **kwargs)
        return result

    B = make_adapter(str, format_b=format_handler)
    b = B("Hello {:s}")

    try:
        print(b.format_b("Pierre"))
        print(b.format("Pierre"))
    except AttributeError as e:
        print("HasAttr:", e)

    C = make_adapter(str, _format_c=format_handler)

    class MyClass(C):

        def make_world_easier(self):
            return self._format_c("World!")

    c = MyClass("Hello {:s}")

    try:
        print(c.make_world_easier())
        print(c.format("World!"))
    except AttributeError as e:
        print("HasAttr:", e)


if __name__ == '__main__':
    main()
