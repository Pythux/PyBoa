
from to_js import to_js


def test_all():
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
