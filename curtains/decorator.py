from functools import wraps
from curtains.operations import Operation

class task(object):
    _task_list = []

    def __init__(self, username=None, password=None, hosts=None, ):
        self.hosts = hosts
        self.username = username
        self.password = password


    def __call__(self, fn):
        self._task_list.append({'hosts': self.hosts, 'username': self.username, 'password':self.password, 'fn': fn})
        @wraps(fn)
        def decorated(*args, **kwargs):
            out = fn(args, kwargs)
            return out
        return decorated

    @classmethod
    def task_list(cls):
        return cls._task_list

