import pytest
from boa import boa, yaml, json, BoaWraps


def test_boa_obj_dict():
    d = {'yo': {'da': 4}, 'li': [{'in_li': 4}, 'str'], 'tuple': ({'tu': 4}, 5)}
    boa_obj = boa(d)
    li_1 = [
        boa_obj.yo, boa_obj.yo.da, boa_obj.li[0].in_li,
        boa_obj.li[1], boa_obj.tuple[0].tu, boa_obj.tuple[1]]
    li_2 = [
        boa_obj['yo'], boa_obj.yo['da'], boa_obj['li'][0].in_li,
        boa_obj.li[1], boa_obj.tuple[0]['tu'], boa_obj.tuple[1]]
    for i in range(len(li_1)):
        assert li_1[i] == li_2[i]

    with pytest.raises(AttributeError):
        boa_obj.new
    with pytest.raises(KeyError):
        boa_obj['another']
    boa_obj.new = 'newVal'
    assert boa_obj.new == 'newVal'
    assert boa_obj['new'] == 'newVal'

    boa_obj['another'] = {'a': 6}
    assert boa_obj.another.a == 6
    boa_obj['another'].a += 4
    assert boa_obj.another.a == 10

    boa_obj.another.a += 6
    assert boa_obj['another'].a == 16
    assert boa_obj['another']['a'] == 16

    boa_obj.another_one = {'b': 8}
    assert boa_obj.another_one.b == 8

    boa_obj['a -> $@" toto'] = 2
    assert boa_obj['a -> $@" toto'] == 2
    boa_obj = boa({'a -> $@" toto': 4, 'a': boa})
    assert boa_obj['a -> $@" toto'] == 4
    assert boa_obj.a == boa
    boa_obj[' -> &'] = {'a': [{'b': 6}]}
    assert boa_obj[' -> &'].a[0].b == 6

    boa_obj = boa({'get': 2})
    assert boa_obj.keys is not None
    boa_obj.keys = 2
    assert boa_obj.keys == 2
    boa_obj.keys += 4
    assert boa_obj['keys'] == 6

    boa_obj.a = 2
    d = boa_obj.toPython()
    with pytest.raises(AttributeError):
        d.a += 1

    a = boa({'li': [1, 2, {'k': 'v'}]})
    a.toPython()['li'][2].__class__ == dict
    assert a.li[2].k == 'v'

    with pytest.raises(AttributeError):
        a.toPython()['li'][2].k

    assert boa_obj.__class__.__name__ == 'Dict'
    assert isinstance(boa_obj, dict)

    boa_obj = boa({})
    with pytest.raises(KeyError):
        boa_obj['a']['b'] = 2
    with pytest.raises(AttributeError):
        boa_obj.a.b = 2

    assert boa_obj.get('a') is None


def test_boa_list():
    li = [1, 2, 3]
    boa_list = boa(li)
    assert li == [1, 2, 3]
    assert boa_list.map(lambda x: x+1) == [2, 3, 4]
    assert boa_list == li

    assert boa_list.reduce(lambda acc, x: acc+x) == 6

    boa_list_2 = boa_list.reverse()
    assert boa_list == li
    assert boa_list_2 == [3, 2, 1]

    assert boa_list_2.index(3) == 0
    assert boa_list_2.index(4, raise_exception=False) is None
    with pytest.raises(ValueError):
        boa_list_2.index(4)

    assert boa_list.index(3) == 2
    assert boa_list.index(3, 1, 2, raise_exception=False) is None
    assert boa_list.index(3, 1, 3) == 2
    assert boa_list.index(3, 1) == 2
    assert boa_list.index(1, 0, 1) == 0
    with pytest.raises(ValueError):
        boa_list.index(3, 0, 1)
    assert boa_list.index(3, 0, 1, raise_exception=False) is None

    li_2 = boa_list.toPython()
    assert li == li_2
    assert hasattr(li, 'map') is False
    assert hasattr(li_2, 'map') is False
    assert hasattr(boa_list, 'map') is True
    l1 = boa([{'a': 2}]).toPython()
    assert hasattr(l1, 'map') is False
    with pytest.raises(AttributeError):
        l1[0].a += 1

    assert boa_list.filter(lambda x: x >= 2) == [2, 3]

    assert boa_list.randomChoice() in boa_list

    shuffled = boa_list.shuffle()
    assert boa_list == li
    for e in shuffled:
        assert e in li

    copy = boa_list.copy()
    assert hasattr(copy, 'map') is True

    copy.append({'a': 2})
    assert copy[-1].a == 2

    assert copy.__class__.__name__ == 'List'
    assert isinstance(copy, list)


def test_json_and_yaml():
    boa_obj = json.loads("""{"a": 4}""")
    assert boa_obj.a == 4
    boa_obj = json.load("""{"b": 6}""")
    assert boa_obj.b == 6
    assert boa_obj.__class__.__name__ == 'Dict'
    assert 'stream' in json.load.__doc__
    assert 'stream' in json.loads.__doc__
    assert "YAML document" in yaml.load.__doc__

    with open('tests/test_data.json') as fd:
        boa_obj = json.load(fd)
        assert boa_obj.a['b'][0].c == "value"
        assert boa_obj.a.b[1] == 4

    with open('tests/test_data.yml') as fd:
        boa_obj = yaml.load(fd)
        assert boa_obj.__class__.__name__ == 'List'
        assert isinstance(boa_obj, list)
        assert boa_obj[0].a == 4
        assert boa_obj[1].b == 2
        assert boa_obj[1].d.e == 6
        assert str(boa_obj) == "[{'a': 4}, {'b': 2, 'c': 3, 'd': {'e': 6}}]"


def test_import_json_yaml():
    import json as json_lib
    import yaml as yaml_lib
    with pytest.raises(AttributeError):
        json_lib.loads("""{"a": 4}""").a
    assert json_lib.loads("""{"a": 4}""")['a'] == 4
    with pytest.raises(AttributeError):
        yaml_lib.load("""a: 2""", yaml_lib.SafeLoader).a
    assert yaml_lib.load("""a: 2""", yaml_lib.SafeLoader)['a'] == 2

    assert yaml.load("""a: 2""").a == 2
    assert yaml.safe_load("""a: 2""").a == 2  # loader for yaml.load
    assert yaml.unsafe_load("""a: 2""").a == 2
    assert yaml.full_load("""a: 2""").a == 2

    assert 'stream' in json.loads.__doc__
    assert 'stream' not in json_lib.loads.__doc__


def test_raise_boa():
    d = boa({'a': 2})
    with pytest.raises(ValueError):
        boa(d)

    assert boa(d, raise_exception=False).__class__.__name__ == 'Dict'


class A:
    """simple doc"""
    x = 2
    d = {'key': 'value'}

    def fun(self, data):
        return data


def test_BoaWraps():
    obj = BoaWraps(A())
    assert obj.x == 2
    assert callable(obj.fun)
    assert obj.__class__.__name__ == 'A'
    assert obj.__class__.__doc__ == 'simple doc'
    assert obj.__doc__ == 'simple doc'
    assert obj.fun(5) == 5
    assert obj.fun({'a': 4}).a == 4
    assert obj.d.key == 'value'
    assert obj.d.__class__.__name__ == 'Dict'

    obj_2 = A()
    with pytest.raises(AttributeError):
        obj_2.fun({'b': 2}).b

    assert obj_2.d.__class__ == dict
    assert obj_2.__class__.__doc__ == 'simple doc'
    assert obj_2.__doc__ == 'simple doc'
    with pytest.raises(AttributeError):
        obj_2.d.key


def test_side_effect():
    d = {'a': {'b': {'c': 1}}}
    boa(d)
    b = boa(d)

    b.toPython()
    assert b.toPython()['a']['b'].__class__ == dict
    boa(boa(boa({'a': {'b': {'c': 1}}}).toPython()).toPython()).toPython()

    li = [[[[1], 2], 3], 4]
    boa(boa(li).toPython())
    boa(li)
    boa(li)


class B:
    def get_nothing(self):
        return None


def test_wraps_obj():
    a = BoaWraps(B())
    assert a.get_nothing() is None
