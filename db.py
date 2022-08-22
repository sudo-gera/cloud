import base64
from typing import Any, overload
from vk import *
import io
import json
import time
from builtins import open

__all__ = ['put', 'get', 'root_get', 'root_set', 'home', 'url','typechecked']


class cache():
    def __init__(self):
        try:
            db = json.loads(
                open(
                    home +
                    '.cloud.cache.json',
                    encoding='utf-8').read())
        except Exception:
            db = []
        self.db = db

    def __del__(self):
        db = self.db
        open(home + '.cloud.cache.json', 'w',
             encoding='utf-8').write(json.dumps(db, indent=1))

    def __getitem__(self, key):
        for w in self.db:
            if w[1] == key:
                w[0] = time.time()
                return base64.b64decode(w[2])

    def __setitem__(self, key, val):
        self.db.append([time.time(), key, base64.b64encode(val).decode()])
        if len(self.db) > 1024:
            self.db.sort()
            self.db[:1] = []


class url:
    def __init__(self, s=''):
        self.s = s

    def __str__(self):
        return self.s

    def __repr__(self):
        return 'url(' + self.s + ')'

    def __bool__(self):
        return bool(self.s)
    
    def __eq__(self,o)->bool:
        print('err')
        assert 0

    def __ne__(self,o)->bool:
        print('err')
        assert 0

@typechecked
def _put(file: io.BytesIO, m: int = 16) -> list[int | str]:
    a: list[int | str] = []
    while (c := file.read(db_max_size)):
        a.append(short_put(c))
    j = json.dumps(a).encode()
    if len(a) > m:
        a = _put(io.BytesIO(j))
        if isinstance(a[0], int):
            a[0] += 1
        else:
            a[:0] = [1]
    return a


@typechecked
def put(data: io.BytesIO | bytes, m: int = 16) -> url:
    if isinstance(data, bytes):
        file = io.BytesIO(data)
    else:
        file = data
    j: str = json.dumps(_put(file, m))
    if isinstance(data, bytes):
        c = cache()
        c[j] = data
    return url(j)


@overload
def get(ua: url, f: io.BytesIO) -> io.BytesIO:
    ...


@overload
def get(ua: url) -> bytes:
    ...


@typechecked
def get(ua: url, f: io.BytesIO | None = None) -> io.BytesIO | bytes:
    a: Any = str(ua)
    q = a
    if f is None:
        ca = cache()
        v = ca[q]
        if v is not None:
            return v
        file = io.BytesIO()
    else:
        file = f
    a = json.loads(a)
    if isinstance(a[0], int):
        c = a[0]
        a = a[1:]
        for w in range(c):
            a = json.loads(b''.join([short_get(w) for w in a]).decode())
    for w in a:
        file.write(short_get(w))
    if f is None:
        file.seek(0)
        v = file.read()
        ca[q] = v
        return v
    return file
