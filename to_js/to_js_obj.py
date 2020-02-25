from functools import reduce


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


def dict_to_js_obj(data):
    if isinstance(data, list) or isinstance(data, tuple):
        return list(map(dict_to_js_obj, data))
    elif isinstance(data, dict):
        return Dict(data)
    else:
        return data


def to_js(data):
    return dict_to_js_obj(data)


def js_to_py(data):
    if isinstance(data, list) or isinstance(data, tuple):
        return list(map(to_dict, data))
    elif isinstance(data, Dict):
        return to_dict(data)
    else:
        return data


def to_dict(js):
    def reducer(acc, k):
        acc[k] = js_to_py(js[k])
        return acc

    return reduce(reducer, js, dict())
