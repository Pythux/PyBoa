from functools import wraps
from .boa_obj import boa
import inspect


def boa_wraps(attribut):
    if inspect.isclass(attribut):
        return attribut
    if not callable(attribut) and boaisable(attribut):
        return boa(attribut)
    if not callable(attribut):
        return BoaWraps(attribut)

    @wraps(attribut)
    def dec(*args, **kwargs):
        return boa_wraps(attribut(*args, **kwargs))
    return dec


def boaisable(data):
    if data is None:
        return True
    if data.__class__.__name__[0].islower():
        return True
    return False


class BoaWraps:
    def __init__(self, obj):
        methods = {
            '__getattribute__': gen__getattribute__(obj),
            '__doc__': obj.__doc__
        }
        self.__class__ = type(obj.__class__.__name__,
                              (obj.__class__,),
                              methods)


def gen__getattribute__(obj):
    def __getattribute__(self, name):
        return boa_wraps(getattr(obj, name))
    return __getattribute__
