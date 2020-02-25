import pytest
from to_js import to_js


def test_dict_to_js():
    d = {'yo': {'da': 4}, 'li': [{'in_li': 4}, 'str'], 'tuple': ({'tu': 4}, 5)}
    js = to_js(d)
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
    js = to_js({'a -> $@" toto': 4, 'a': to_js})
    assert js['a -> $@" toto'] == 4
    assert js.a == to_js
    js[' -> &'] = {'a': [{'b': 6}]}
    assert js[' -> &'].a[0].b == 6

    js = to_js({'get': 2})
    assert js.keys is not None
    js.keys = 2
    assert js.keys == 2
    js.keys += 4
    assert js['keys'] == 6


def test_js_list():
    li = [1, 2, 3]
    js_list = to_js(li)
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
    l1 = to_js([{'a': 2}]).toPython()
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
