# PyBoa

[![Latest Version](https://img.shields.io/pypi/v/PyBoa.svg)](https://pypi.python.org/pypi/PyBoa/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/PyBoa.svg)](https://pypi.python.org/pypi/PyBoa/)


Subclass of list and dict, recursively, giving attribute access and helper functions


### import boa
```python
>>> from boa import boa
```

```python
# recursively transforme the data into boa
>>> a = boa({'b': {'c': [2, 3]}})

# make it accessible by key or attribute
>>> a['b']['c']
[2, 3]
>>> a.b.c
[2, 3]
```



## Do what you usually do

``boa`` return a subclass of ``dict`` and ``list``, letting you do everything you use to do


## everything in [doc: list, dict](https://docs.python.org/3/tutorial/datastructures.html) can still be done

### with the exception of overided methodes:

##### list.reverse
```py
>>> li = boa([1, 2])
>>> li.reverse()
[2, 1]
>>> li # no change in the original list
[1, 2]

# behaviour of list.reverse:
>>> li.reverse(side_effect=True)
>>> li
[2, 1]
# or use list.reverse directly
>>> li = boa([1, 2])
>>> list.reverse(li)
>>> li
[2, 1]
```

##### list.copy
```py
>>> b = boa([1, {'d': 3}])
>>> c = b.copy()
>>> b[0] = 100

# c is a copy of b, and still a boa object:
>>> c[0]
1
>>> c[1].d
3
```

## improvement:
##### list.index
```py
>>> li = boa([1, 2])
>>> li.index(4)  # same behaviour as the original
ValueError: 4 is not in list

>>> li.index(4, raise_exception=False)  # improvement
None
```

## transforme inserted data too:
```py
>>> a = boa({})
>>> a.x = {'y': {'z': 3}}
>>> a.x.y.z
3
>>> a.li = []
>>> a.li.append({'b': 2})
>>> a.li[0].b
2
>>> a['b'] = [{'li': [1, 2]}]
>>> a.b[0].li.map(lambda x: x+1)
[2, 3]
```

## Add some usefull functions
### on list:
#### .map & .filter
```python
>>> li = boa([1, 2])
>>> li.map(lambda x: x+1)
[2, 3]

>>> li = boa([x for x in range(10)])
>>> li.filter(lambda x: 1 < x <= 4)
[2, 3, 4]

# .filter & .map return boa list
>>> li = boa([{'x': x} for x in range(10)])
>>> li.filter(lambda obj: obj.x < 2).map(lambda obj: obj.x)
[0, 1]
```

#### .reduce
```py
>>> li = boa([2, 3])
>>> li.reduce(lambda acc, x: acc*x)
6
```

#### random with .shuffle & .randomChoice
```py
>>> arr = boa([x for x in range(10)])
>>> arr.shuffle()
[3, 1, 5, 8, 6, 2, 0, 7, 9, 4]

>>> arr.randomChoice()
4
# ``one of the element at random``
```

#### returning back to normal dict and list:
```py
>>> a = boa({'li': [1, 2, {'k': 'v'}]})
>>> b = a.toPython()

>>> b.li
AttributeError: 'dict' object has no attribute 'li'
>>> b['li'].map()
AttributeError: 'list' object has no attribute 'map'
>>> b['li'][2].k
AttributeError: 'dict' object has no attribute 'k'
```

## Overide attribute:
```py
# can overide dictionary attributes, if you really want it:
>>> d = boa({'items': 1})
>>> d.keys = 2
>>> d.values()
dict_values([1, 2])
```

## A wraps function
```py
>>> @boa
>>> def fun(x):
>>>     return x

>>> fun({'a': 1}).a
1
```
### wraps objet ?

```py
class A:
    """simple doc"""
    d = {'key': 'value'}

    def fun(self, data):
        return data
```

```py
>>> obj = boa(A())
# keep the class name and doc informations:
>>> obj.__class__.__name__
'A'
>>> obj.__doc__
'simple doc'
>>> obj.fun({'a': {'b': 4}}).a.b
4
>>> obj.d.key
'value'

# no side effect on class A:
>>> obj_2 = A()
>>> obj_2.fun({'b': 2}).b
AttributeError: 'dict' object has no attribute 'b'
>>> obj_2.d.key
AttributeError: 'dict' object has no attribute 'key'
```

#### to the moon !
```py
class B:
    def get_a(self):
        return A()

    def get_b(self):
        return B()
```

```py
>>> b = boa(B())
>>> b.get_a().d.key
'value'
>>> b.get_b().get_b().get_a().d.key
'value'
```
