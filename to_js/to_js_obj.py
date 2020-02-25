import random
import functools


class Dict(dict):
    def __init__(self, d):
        for k, v in d.items():
            d[k] = dict_to_js_obj(v)
        super().__init__(d)

    def __getattribute__(self, name):
        if name in dict.keys(self):
            return dict.get(self, name)
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        return dict.get(self, name)

    def __setattr__(self, name, value):
        js = dict_to_js_obj(value)
        dict.update(self, {name: js})

    def __getitem__(self, key):
        return dict.get(self, key)

    def __setitem__(self, key, value):
        js = dict_to_js_obj(value)
        dict.update(self, {key: js})

    def toPython(self):
        return to_py(self)


class List(list):
    def __init__(self, li):
        super().__init__(map(dict_to_js_obj, li))

    def map(self, fun):
        return List(map(fun, self))

    def reduce(self, fun):
        return functools.reduce(fun, self)

    def filter(self, fun):
        return List(filter(fun, self))

    def index(self, elem, *args, raise_exception=False):
        try:
            return super().index(elem, *args)
        except ValueError as e:
            if raise_exception:
                raise e
            return None

    def reverse(self):
        return List(self[::-1])

    def shuffle(self):
        li = self[:]
        random.shuffle(li)
        return li

    def randomTake(self):
        return random.choice(self)

    def copy(self):
        return List(self[:])

    def append(self, el):
        list.append(self, to_js(el))

    def toPython(self):
        return to_py(self)


def dict_to_js_obj(data):
    if isinstance(data, list) or isinstance(data, tuple):
        return List(map(dict_to_js_obj, data))
    elif isinstance(data, dict):
        return Dict(data)
    else:
        return data


def to_js(data):
    return dict_to_js_obj(data)


def to_py(data):
    if isinstance(data, List):
        return list(map(to_py, data))
    elif isinstance(data, Dict):
        return to_dict(data)
    else:
        return data


def to_dict(js):
    def reducer(acc, k):
        acc[k] = to_py(js[k])
        return acc
    return functools.reduce(reducer, js, dict())
