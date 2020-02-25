from functools import wraps
from .boa_obj import to_boa

json = None
yaml = None


def make_json_load(json_loads):
    def load(stream, **kw):
        """
            ``stream`` is ``string`` or have ``.read()`` like an ``fp``
            :return: the corresponding Python object
        """
        if hasattr(stream, 'read'):
            stream = stream.read()
        return json_loads(stream, **kw)
    return load


def decorate_boa(fun):
    @wraps(fun)
    def dec(*args, **kwargs):
        return to_boa(fun(*args, **kwargs))
    return dec


try:
    import json
    json.load = decorate_boa(make_json_load(json.loads))
    json.loads = json.load
except ImportError:
    pass

try:
    import yaml
    yaml.load = decorate_boa(yaml.load)
    yaml.safe_load = decorate_boa(yaml.safe_load)
except ImportError:
    pass
