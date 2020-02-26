# PyBoa

Change Python dict and list recursively, making Data Structures where keys can be accessed by attribut.
Add some usefull functions and an object wraper

```python
from boa import boa


# recursively transforme the data into boa:
a = boa({'b': {'c': 2}})

# can be accessed by key or attribute:
assert a.b.c == a['b']['c']

# transforme inserted data into boa too:
a.x = {'y': {'z': 3}}
assert a.x.y.z == 3

# a.x = {...} and a['x'] = {...} will do the same
a['li'] = [{'k': 1}]
assert a.li[0].k == 1

# boa list and dict are instance of list, dict:
assert isinstance(boa([]), list)
assert isinstance(boa({}), dict)

# have a .map .reduce in list:
a = boa({'b': [[1, 2, 3], [1, 2]]})
assert a.b.map(lambda li: li.reduce(lambda x, y: x + y)) == [6, 3]

a['li'] = [{'k': 1}, {'k': 2}]
assert a.li.map(lambda obj: obj.k) == [1, 2]


# can overide dictionary attributes:
d = boa({})
d.keys = 2
d.keys += 1
assert list(d.values()) == [3]


# now, time for BoaWraps:
from boa import BoaWraps


# let have a simple class:
class A:
    """simple doc"""
    d = {'key': 'value'}

    def fun(self, data):
        return data

# if we `BoaWraps` an instance of a class, it will produce boa:
obj = BoaWraps(A())

# keep the class name and all of the class information:
assert obj.__class__.__name__ == 'A'
assert obj.__class__.__doc__ == 'simple doc'
assert obj.__doc__ == 'simple doc'

# the function `fun` return boa:
assert obj.fun({'a': {'b': 4}}).a.b == 4
# and the attribute `d` too:
assert obj.d.key == 'value'


# the class A is not modified:
obj_2 = A()

# no boa here:
import pytest
with pytest.raises(AttributeError):
    obj_2.fun({'b': 2}).b

with pytest.raises(AttributeError):
    obj_2.d.key


# a little more complicated class
class B:
    def get_a(self):
        return A()

    def get_b(self):
        return B()


b = BoaWraps(B())
assert b.get_a().d.key == 'value'
assert b.get_b().get_b().get_a().d.key == 'value'

```
