from __future__ import annotations

from inspect import isfunction


def dotval(obj, dottedpath, default=None):
    """
    Возвращает значение аттрибута объекта или элемента словаря по его пути в формате 'a.b.c'
    Примеры:
    obj = {'item1': {'nested': 123, 'other': 456}}
    >>> dotval(obj, "item1.nested")
    123
    >>> dotval(obj, "item2")
    None
    """
    val = obj
    sentinel = object()
    for attr in dottedpath.split("."):
        if isinstance(val, dict):
            val = val.get(attr, sentinel)
            if val is sentinel:
                return default
        elif not hasattr(val, attr):
            return default
        else:
            val = getattr(val, attr, sentinel)
            if val is sentinel:
                return default
            if isfunction(val):
                val = val()
    return val
