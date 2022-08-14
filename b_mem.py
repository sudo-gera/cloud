from functools import *
from random import *
from time import sleep
import json
from db import *

def treeprint(*a):
    pass

class load:
    pass

load=load()

load.get=get
load.put=put

__all__=['d','put','get','b','load','root_set','root_get']

class l:

    def __init__(self, r, t=None):
        self.r = r
        self.l = t.l if isinstance(t, l) else t if t is not None else []

    def __getitem__(self, k):
        return self.l[k]

    def __len__(self):
        return len(self.l)

    def index(self, v):
        return self.l.index(v)

    def cl(self):
        return self.l[:]

    def __repr__(self):
        return 'l'+repr(self.l)

class n:

    def __init__(self, r, t=None):
        self.r = r
        self.n = t.n if isinstance(t, n) else t if t is not None else []

    def __getitem__(self, k):
        t = self.n[k]
        r = t
        if not isinstance(t, list):
            r = [r]
        r = [w if isinstance(w, node) else node(key=w) if w is not None else w for w in r]
        if not isinstance(t, list):
            r = r[0]
        return r

    def __len__(self):
        return len(self.n)

    def index(self, v):
        return self.n.index(v)

    def cl(self):
        return self.n[:]

    def __repr__(self):
        return 'n'+repr(self.n)

max_len = 64

class node:

    def __repr__(self):
        return 'node'+repr((self._data,self._next))

    def __init__(self, *, data=None, next=None, key=None):
        self._data = l(self, data) if data is not None else None
        self._next = n(self, next) if next is not None else None
        self.key = key

    @property
    def next(self):
        if self._next==None:
            n=loads(self.key)
            self._next,self._data=n._next,n._data
        return self._next

    @property
    def data(self):
        if self._data==None:
            n=loads(self.key)
            self._next,self._data=n._next,n._data
        return self._data


def upd(self):
    if type(self) in [str, type(None)]:
        return self
    if self.key!=None:
        return self.key
    self._next.n = [upd(w) for w in self._next.n]
    return dumps(self)


def dumps(q):
    if q.key is not None:
        return q.key
    r = {
        'data': [list(w) if isinstance(w, item) else [w] for w in q.data.l],
        'next': q.next.n
    } if q is not None else q
    r = json.dumps(r).encode()
    return load.put(r)


def loads(q):
    if type(q)==node:
        return q
    z = q
    q = load.get(q)
    q = json.loads(q.decode())
    if q is not None:
        q['data'] = [item(*w) if len(w) == 2 else w[0] for w in q['data']]
    return node(**q, key=z) if q is not None else q




def check(self, r=1):
    assert len(self.data) + 1 == len(self.next)
    assert len(self.data) <= max_len
    if self.next[0] is None:
        assert list(self.data) == sorted(self.data)
    assert r or max_len // 2 <= len(self.data)
    if self.next[0] is None:
        return [self.data[0], self.data[-1]]
    a = [check(w, 0) for w in self.next]
    for w in range(len(self.data)):
        assert a[w][1] < self.data[w] < a[w + 1][0]
    return [a[0][0], a[-1][1]]


def insert(self, k):
    if k in self.data:
        t = self.data.index(k)
        self = node(next=self.next, data=self.data[:t] + [k] + self.data[t + 1:])
    elif self.next[0] is None:
        w = 0
        while w < len(self.data) and self.data[w] < k:
            w += 1
        self = node(data=self.data[:w] + [k] + self.data[w:], next=[None] + self.next.cl())
    else:
        w = 0
        while w < len(self.data) and self.data[w] < k:
            w += 1
        self = node(data=self.data, next=self.next[:w] +
                 [insert(self.next[w], k)] + self.next[w + 1:])
        if len(self.next[w].data) > max_len:
            assert len(self.next[w].data) == 1 + max_len
            q = self.next[w]
            a = node(data=q.data[:max_len // 2],
                     next=q.next[:max_len // 2 + 1])
            d = q.data[max_len // 2]
            q = node(data=q.data[max_len // 2 + 1:],
                     next=q.next[max_len // 2 + 1:])
            self = node(next=self.next[:w] + [a, q] + self.next[w + 1:],
                     data=self.data[:w] + [d] + self.data[w:])
    return self


def find(self, k):
    if k in self.data:
        return [[self, self.data.index(k)]]
    if self.next[0] is None:
        return None
    w = 0
    while w < len(self.data) and self.data[w] < k:
        w += 1
    r = find(self.next[w], k)
    if r is not None:
        r.append([self, w])
    return r


def erase(self, k):
    if self.next[0] is None:
        t = self.data.index(k)
        self = node(data=self.data[:t] + self.data[t + 1:], next=self.next[1:])
    else:
        w = 0
        while w < len(self.data) and self.data[w] < k:
            w += 1
        self = node(data=self.data, next=self.next[:w] +
                 [erase(self.next[w], k)] + self.next[w + 1:])
        if len(self.next[w].data) < max_len // 2:
            assert len(self.next[w].data) == max_len // 2 - 1
            if w:
                if len(self.next[w - 1].data) == max_len // 2:
                    self = node(data=self.data, next=self.next[:w -
                                                      1] +
                             [node(data=self.next[w -
                                               1].data.cl() +
                                   [self.data[w -
                                           1]] +
                                   self.next[w].data.cl(), next=self.next[w -
                                                                    1].next.cl() +
                                   self.next[w].next.cl())] +
                             self.next[w:])
                    self = node(data=self.data[:w - 1] + self.data[w:],
                             next=self.next[:w] + self.next[w + 1:])
                else:
                    self = node(data=self.data,
                             next=self.next[:w] + [node(data=[self.data[w - 1]] + self.next[w].data.cl(),
                                                     next=[self.next[w - 1].next[-1]] + self.next[w].next.cl())] + self.next[w + 1:])
                    self = node(
                        next=self.next, data=self.data[:w - 1] + [self.next[w - 1].data[-1]] + self.data[w:])
                    self = node(data=self.data,
                             next=self.next[:w - 1] + [node(data=self.next[w - 1].data[:-1],
                                                         next=self.next[w - 1].next[:-1])] + self.next[w:])
            elif len(self.next[w + 1].data) == max_len // 2:
                self = node(data=self.data, next=self.next[:w] +
                         [node(data=self.next[w].data.cl() +
                               [self.data[w]] +
                               self.next[w +
                                      1].data.cl(), next=self.next[w].next.cl() +
                               self.next[w +
                                      1].next.cl())] +
                         self.next[w +
                                1:])
                self = node(data=self.data[:w] + self.data[w + 1:],
                         next=self.next[:w + 1] + self.next[w + 2:])
            else:
                self = node(data=self.data,
                         next=self.next[:w] + [node(data=self.next[w].data.cl() + [self.data[w]],
                                                 next=self.next[w].next.cl() + [self.next[w + 1].next[0]])] + self.next[w + 1:])
                self = node(next=self.next,
                         data=self.data[:w] + [self.next[w + 1].data[0]] + self.data[w + 1:])
                self = node(data=self.data,
                         next=self.next[:w + 1] + [node(data=self.next[w + 1].data[1:],
                                                     next=self.next[w + 1].next[1:])] + self.next[w + 2:])
    return self


def to_list(self, l):
    if self.next[0] is None:
        for w in self.data:
            l.append(w)
    else:
        to_list(self.next[0], l)
        for w in range(len(self.data)):
            l.append(self.data[w])
            to_list(self.next[w + 1], l)
    return l


def chval(self, a, t, d, n):
    if n:
        v = a[n][1]
        self = node(data=self.data,
                 next=self.next[:v] + [chval(self.next[v],
                                          a,
                                          t,
                                          d,
                                          n - 1)] + self.next[v + 1:])
    else:
        self = node(next=self.next, data=self.data[:t] + [d] + self.data[t + 1:])
    return self


class b:

    def __init__(self,s=None):
        self.s = None
        if s!=None:
            self.s=get(s).decode()

    def check(self):
        return
        if self.s is not None:
            check(self.s)

    def add(self, v):
        self.check()
        r = loads((self.s)) if self.s is not None else self.s
        q = node(data=[], next=[r])
        q = insert(q, v)
        r = q
        if not r.data:
            r = r.next[0]
        # r = upd(r)
        self.s = r
        # self.s=(dumps(r)) if r!=None else r
        self.check()

    def find(self, v):
        self.check()
        r = loads((self.s)) if self.s is not None else self.s
        if r is None:
            return []
        f = find(r, v)
        if f is None:
            return []
        f = f[0][0]
        return [f.data[f.data.index(v)]]

    def remove(self, v):
        self.check()
        r = loads((self.s)) if self.s is not None else self.s
        if r is None:
            return
        a = find(r, v)
        if a is None:
            return
        a = a[::-1]
        if a[-1][0].next[0] is not None:
            t = a[-1][0].next[a[-1][0].data.index(v) + 1]
            while t.next[0] is not None:
                t = t.next[0]
            d = t.data[0]
            r = erase(r, d)
            a = find(r, v)
            t = a[0][0].data.index(v)
            r = chval(r, a, t, d, len(a) - 1)
        else:
            r = erase(r, v)
        if len(r.data) == 0:
            r = r.next[0]
        # r = upd(r)
        self.s = r
        # self.s=(dumps(r)) if r!=None else r
        self.check()

    def __repr__(self):
        r = loads((self.s)) if self.s is not None else self.s
        treeprint(r)
        return ''

    def to_list(self):
        r = loads((self.s)) if self.s is not None else self.s
        if r is None:
            return []
        return to_list(r, [])

    def getstr(self,d=0):
        self.s=upd(self.s)
        if d==0:
            return put(self.s.encode(),m=1)

    def __del__(self):
        self.getstr(d=1)

@total_ordering
class item:

    def __init__(self, k, v=None):
        self.k = k
        self.v = v

    def __lt__(self, o):
        return self.k < o.k

    def __eq__(self, o):
        return self.k == o.k

    def __repr__(self):
        return 'item' + repr([self.k, self.v])

    def __getitem__(self, n):
        return [self.k, self.v][n]

class d:

    def __init__(self,s=None):
        self.b = b(s)

    def __getitem__(self, k):
        return self.b.find(item(k))[0].v

    def __setitem__(self, k, v):
        self.b.add(item(k, (v)))

    def __delitem__(self, k):
        self.b.remove(item(k))

    def __repr__(self):
        return repr(self.b)

    def __contains__(self, k):
        return bool(self.b.find(item(k)))

    def to_dict(self):
        return dict(self.b.to_list())

    def getstr(self):
        return self.b.getstr()

if __name__ == '__main__':

    to_sleep = 0

    data = {}

    def put(v):
        sleep(to_sleep)
        k = ''
        while not k or k in data:
            k = ''.join(
                [
                    chr(
                        randint(32, 126)
                    ) for w in range(
                        randint(128, 1024)
                    )
                ]
            )
        data[k] = v
        return k


    def get(k):
        sleep(to_sleep)
        return data[k]

    load.get=get
    load.put=put

    self = b()
    sed = randint(-9999, 9999)
    print(sed)
    seed(sed)
    a = set()
    for w in range(99):
        q = choice([0] * 3 + [1] + [2])
        if q == 0:
            r = randint(-9999, 9999)
            a.add(r)
            self.add(r)
        if q == 1:
            r = choice(list(a)) if a and randint(0, -1 + 2) else randint(0, -1 + 9)
            assert (r in a) == bool(self.find(r))
            assert r not in a or self.find(r)[0] == r
        if q == 2 and a:
            r = choice(list(a))
            a.remove(r)
            self.remove(r)
        f = set(self.to_list())
        assert a == f
    a = dict()
    self = d()
    for w in range(99):
        q = choice([0] * 3 + [1] + [2] + [3])
        if q == 0:
            k = choice(list(a)) if a and randint(0, 1) else randint(-9999, 9999)
            v = randint(-9999, 9999)
            a[k] = v
            self[k] = v
        if q == 1:
            k = choice(list(a)) if a and randint(0, 1) else randint(-9999, 9999)
            assert (k in a) == (k in self)
        if q == 2 and a:
            k = choice(list(a))
            a[k] == self[k]
        if q == 3 and a:
            k = choice(list(a))
            del a[k]
            del self[k]
        assert self.to_dict() == a

    a = dict()
    self = d()
    for w in range(999):
        k = randint(-9999, 9999)
        v = randint(-9999, 9999)
        self[k] = v
        a[k] = v

    to_sleep = 0.1
    for w in range(19):
        q = choice([0] + [1] + [2] + [3])
        if q == 0:
            k = choice(list(a)) if a and randint(0, 1) else randint(-9999, 9999)
            v = randint(-9999, 9999)
            a[k] = v
            self[k] = v
        if q == 1:
            k = choice(list(a)) if a and randint(0, 1) else randint(-9999, 9999)
            assert (k in a) == (k in self)
        if q == 2 and a:
            k = choice(list(a))
            a[k] == self[k]
        if q == 3 and a:
            k = choice(list(a))
            del a[k]
            del self[k]
