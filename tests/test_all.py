import pytest
import json as json_lib
import yaml as yaml_lib
from boa import boa, yaml, json


def test_js_dict():
    d = {'yo': {'da': 4}, 'li': [{'in_li': 4}, 'str'], 'tuple': ({'tu': 4}, 5)}
    js = boa(d)
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

    js.another.a += 6
    assert js['another'].a == 16
    assert js['another']['a'] == 16

    js.another_one = {'b': 8}
    assert js.another_one.b == 8

    js['a -> $@" toto'] = 2
    assert js['a -> $@" toto'] == 2
    js = boa({'a -> $@" toto': 4, 'a': boa})
    assert js['a -> $@" toto'] == 4
    assert js.a == boa
    js[' -> &'] = {'a': [{'b': 6}]}
    assert js[' -> &'].a[0].b == 6

    js = boa({'get': 2})
    assert js.keys is not None
    js.keys = 2
    assert js.keys == 2
    js.keys += 4
    assert js['keys'] == 6

    js.a = 2
    d = js.toPython()
    with pytest.raises(AttributeError):
        d.a += 1

    assert js.__class__.__name__ == 'Dict'
    assert isinstance(js, dict)

    js = boa({})
    with pytest.raises(TypeError):
        js['a']['b'] = 2


def test_js_list():
    li = [1, 2, 3]
    js_list = boa(li)
    assert li == [1, 2, 3]
    assert js_list.map(lambda x: x+1) == [2, 3, 4]
    assert js_list == li

    assert js_list.reduce(lambda acc, x: acc+x) == 6

    js_list_2 = js_list.reverse()
    assert js_list == li
    assert js_list_2 == [3, 2, 1]

    assert js_list_2.index(3) == 0
    assert js_list_2.index(4) is None
    assert js_list.index(3) == 2
    assert js_list.index(3, 1, 2) is None
    assert js_list.index(3, 1, 3) == 2
    assert js_list.index(3, 1) == 2
    assert js_list.index(1, 0, 1) == 0
    assert js_list.index(3, 0, 1) is None

    li_2 = js_list.toPython()
    assert li == li_2
    assert hasattr(li, 'map') is False
    assert hasattr(li_2, 'map') is False
    assert hasattr(js_list, 'map') is True
    l1 = boa([{'a': 2}]).toPython()
    assert hasattr(l1, 'map') is False
    with pytest.raises(AttributeError):
        l1[0].a += 1

    assert js_list.filter(lambda x: x >= 2) == [2, 3]

    assert js_list.randomTake() in js_list

    shuffled = js_list.shuffle()
    assert js_list == li
    for e in shuffled:
        assert e in li

    copy = js_list.copy()
    assert hasattr(copy, 'map') is True

    copy.append({'a': 2})
    assert copy[-1].a == 2

    assert copy.__class__.__name__ == 'List'
    assert isinstance(copy, list)


def test_json_and_yaml():
    assert json is not None  # import json success
    js = json.loads("""{"a": 4}""")
    assert js.a == 4
    js = json.load("""{"b": 6}""")
    assert js.b == 6
    assert js.__class__.__name__ == 'Dict'
    assert 'stream' in json.load.__doc__
    assert 'stream' in json.loads.__doc__
    assert "YAML document" in yaml.load.__doc__

    with open('tests/test_data.json') as fd:
        js = json.load(fd)
        assert js.a['b'][0].c == "value"
        assert js.a.b[1] == 4
