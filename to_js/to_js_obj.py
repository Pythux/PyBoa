from functools import reduce


# first
def non_recursive_imutable_dict_to_js_obj(d):
    from collections import namedtuple
    return namedtuple("JS", d.keys())(*d.values())


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


def tests():
    d = {'yo': {'da': 4}, 'li': [{'in_li': 4}, 'str'], 'tuple': ({'tu': 4}, 5)}
    js = dict_to_js_obj(d)
    li_1 = [js.yo, js.yo.da, js.li[0].in_li, js.li[1], js.tuple[0].tu, js.tuple[1]]
    li_2 = [js['yo'], js.yo['da'], js['li'][0].in_li, js.li[1], js.tuple[0]['tu'], js.tuple[1]]
    for i in range(len(li_1)):
        assert li_1[i] == li_2[i]

    assert js.new is None
    js.new = 'newVal'
    assert js.new == 'newVal'
    assert js['another'] is None
    js['another'] = {'a': 6}
    assert js.another.a == 6
    js['another'].a += 4
    assert js.another.a == 10

    js.another_one = {'b': 8}
    assert js.another_one.b == 8

    js['a -> $@" toto'] = 2
    assert js['a -> $@" toto'] == 2
    js = dict_to_js_obj({'a -> $@" toto': 4, 'a': dict_to_js_obj})
    assert js['a -> $@" toto'] == 4
    assert js.a == dict_to_js_obj

    js = to_js({'get': 2})
    assert js.keys is not None
    js.keys = 2
    assert js.keys == 2
    js.keys += 4
    assert js['keys'] == 6
    print('pass all tests')


if __name__ == '__main__':
    tests()
