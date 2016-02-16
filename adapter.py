# -*- coding: utf-8 -*-
"""Module: adapter.py

Coomunication standardisée entre API
"""
from functools import partial, partialmethod


class AdapterFactory(object):

    class Adapter(object):

        subject = None
        instance = None

        def __str__(self):
            if self.instance is not None:
                return str(self.instance)
            elif self.subject is not None:
                return str(self.subject)
            else:
                return super().__str__()

        def __repr__(self):
            if self.instance is not None:
                return repr(self.instance)
            elif self.subject is not None:
                return repr(self.subject)
            else:
                return super().__repr__()

    class Proxy(object):

        def __init__(self, name, method):
            self.name = name
            self.method = method

        def __get__(self, adapter, objtype=None):
            if adapter.instance is not None:
                method = getattr(adapter.instance, self.method)
                if callable(method):
                    method = partial(method)
            elif adapter.subject is not None:
                method = getattr(adapter.subject, self.method)
                if callable(method):
                    method = partial(method)

            return method

        def __set__(self, adapter, value):
            subject = object.__getattribute__(adapter, 'subject')
            setattr(subject, self.method, value)

        def __delete__(self, adapter):
            subject = object.__getattribute__(adapter, 'subject')
            delattr(subject, self.method)

    def __init__(self, *args, **kwargs):
        self.what = 'Adapter'
        self.methods = {}

    def create_adapter(self):
        adapter = type(self.what, (self.Adapter,), self.methods)
        return adapter


class AdapterBuilder(object):

    def __init__(self):
        self.factory = None

    def setup_subject(self, subject):
        self.factory = AdapterFactory()
        self.factory.methods['subject'] = subject

    def setup_initializer(self, initializer=None):
        if initializer is None:
            def initializer(self, *args, **kwargs):
                self.instance = self.subject(*args, **kwargs)

        self.factory.methods['__init__'] = partialmethod(initializer)

    def add_method(self, item, handler):
        self.factory.methods[item] = self.factory.Proxy(item, handler)

    def make_adapter(self):
        return self.factory.create_adapter()


class AdapterEngine(object):

    def __init__(self):
        self.builder = None

    def build(self, subject, methods, initializer=None):
        self.builder = AdapterBuilder()
        self.builder.setup_subject(subject)
        self.builder.setup_initializer(initializer)
        for item, handler in methods.items():
            self.builder.add_method(item, handler)
        return self

    @property
    def adapter(self):
        return self.builder.make_adapter()


class StringEngine(AdapterEngine):

    def build(self):
        subject = str
        initializer = None
        methods = {"format_a": "format"}
        return super().build(subject, methods, initializer)


def main():
    adapted = StringEngine().build().adapter
    print(adapted("toto {:s}").format_a("l'escargot"))
    print("--- Fin du programme ---")


if __name__ == '__main__':
    main()
