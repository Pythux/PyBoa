from boa import boa


class L(list):
    def fun_id(self, x):
        return x

    def __str__(self):
        return 'li({})'.format(self.__repr__())


def test_list_subclass():
    li = boa(L([1, 2]))
    assert li.__class__ == L
    assert repr(li) == '[1, 2]'
    assert str(li) == 'li([1, 2])'
    assert li[0] == 1
    assert li == [1, 2]
    assert li.fun_id({'a': 3}).a == 3
    assert li.fun_id(L([{'a': 2}]))[0].a == 2
