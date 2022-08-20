from abc import ABCMeta, abstractmethod
import functools
import time
import json
import typing
import random
# if __name__!='__main__'
#     from db import *

def treeprint(*a):
    pass

exec(open('../c/treeprint.py').read())


__all__ = ['d', 'put', 'get', 'root_set', 'root_get', 'home']

# class l:

#     def __init__(self, r, t=None):
#         self.r = r
#         self.l = t.l if isinstance(t, l) else t if t is not None else []

#     def __getitem__(self, k):
#         return self.l[k]

#     def __len__(self):
#         return len(self.l)

#     def index(self, v):
#         return self.l.index(v)

#     def cl(self):
#         return self.l[:]

#     def __repr__(self):
#         return 'l'+repr(self.l)

# class n:

#     def __init__(self, r, t=None):
#         self.r = r
#         self.n = t.n if isinstance(t, n) else t if t is not None else []

#     def __getitem__(self, k):
#         return self.n[k]

#     def __len__(self):
#         return len(self.n)

#     def index(self, v):
#         return self.n.index(v)

#     def cl(self):
#         return self.n[:]

#     def __repr__(self):
#         return 'n'+repr(self.n)


class assigner:
    def __init__(self, **d):
        self.__dict__ |= d

    def __getitem__(self, n):
        return assigner(n=n, **self.__dict__)

    def __lshift__(self, v):
        return assigner(v=v, **self.__dict__)


data = assigner(s='data')
next = assigner(s='next')

max_len = 2


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: typing.Any) -> bool: ...


T = typing.TypeVar('T', bound=Comparable)


class node(typing.Generic[T]):

    # def __repr__(self):
    #     return 'node'+repr((self._data,self._next))

    def __init__(self,
                 *,
                 data: list[T] | tuple[T,
                                          ...] | None = None,
                 next: 'list[node[T]]|tuple[node[T],...]|None' = None,
                 key: str = None):
        self._data = tuple(data) if data is not None else None
        self._next = tuple(next) if next is not None else None
        self.key = key

    def load(self):
        if self._next is None or self._data is None:
            n = loads(self.key)
            self._next, self._data = n._next, n._data
            self._next = tuple(
                [w if isinstance(w, node | None) else node(key=w) for w in self._next])

    @property
    def next(self) -> 'tuple[node[T],...]':
        self.load()
        assert isinstance(self._next, tuple)
        return self._next

    @property
    def data(self) -> tuple[T, ...]:
        self.load()
        assert isinstance(self._data, tuple)
        return self._data

    def __ilshift__(self, a):
        data, next = list(self.data), list(self.next)
        exec(f'{a.s}[a.n]=a.v')
        del a.n, a.v
        return node(data=data, next=next)


@typing.overload
def upd(self: node | str) -> str:
    ...


@typing.overload
def upd(self: None) -> None:
    ...


def upd(self: node[T] | str | None) -> str | None:
    if isinstance(self, str) or self is None:
        return self
    assert isinstance(self, node)
    if self.key is not None:
        return self.key
    assert self._next is not None
    assert self._data is not None
    z: typing.Any = 0
    r = {
        'data': tuple([item(w).to_list() if isinstance(w, item) else [w] for w in self._data]),
        'next': tuple([upd(w) for w in self._next])
    } if self is not None else None
    er = json.dumps(r).encode()
    return put(er)


def loads(self: node[T] | str) -> node | None:
    if isinstance(self, node) or self is None:
        return self
    assert isinstance(self, str)
    z = self
    qd = json.loads(get(z).decode())
    if qd is not None:
        qd['data'] = [item(*w) if len(w) == 2 else w[0]
                         for w in qd['data']]
    return node(**qd, key=z) if qd is not None else qd


# def check(self, r=1):
#     assert len(self.data) + 1 == len(self.next)
#     assert len(self.data) <= max_len
#     if self.next[0] is None:
#         assert list(self.data) == sorted(self.data)
#     assert r or max_len // 2 <= len(self.data)
#     if self.next[0] is None:
#         return [self.data[0], self.data[-1]]
#     a = [check(w, 0) for w in self.next]
#     for w in range(len(self.data)):
#         assert a[w][1] < self.data[w] < a[w + 1][0]
#     return [a[0][0], a[-1][1]]


def insert(self:node[T], k:T):
    if k in self.data:
        t = self.data.index(k)
        self = node(next=self.next, data=self.data[:t] + (k,) + self.data[t + 1:])
    elif self.next[0] is None:
        w = 0
        while w < len(self.data) and self.data[w] < k:
            w += 1
        self = node(data=self.data[:w] + (k,) + self.data[w:], next=(None,) + self.next)
    else:
        w = 0
        while w < len(self.data) and self.data[w] < k:
            w += 1
        self = node(data=self.data, next=self.next[:w] +
                 (insert(self.next[w], k),) + self.next[w + 1:])
        if len(self.next[w].data) > max_len:
            assert len(self.next[w].data) == 1 + max_len
            q = self.next[w]
            a = node(data=q.data[:max_len // 2],
                     next=q.next[:max_len // 2 + 1])
            d = q.data[max_len // 2]
            q = node(data=q.data[max_len // 2 + 1:],
                     next=q.next[max_len // 2 + 1:])
            self = node(next=self.next[:w] + (a, q,) + self.next[w + 1:],
                     data=self.data[:w] + (d,) + self.data[w:])
    return self


def find(self: node[T], k: T) -> list[tuple[node[T], int]]:
    if k in self.data:
        return [(self, self.data.index(k))]
    if self.next[0] is None:
        return None
    w = 0
    while w < len(self.data) and self.data[w] < k:
        w += 1
    r = find(self.next[w], k)
    if r is not None:
        r.append((self, w))
    return r


def erase(self:node[T], k:T)->node[T]:
    if self.next[0] is None:
        t = self.data.index(k)
        self = node(data=self.data[:t] + self.data[t + 1:], next=self.next[1:])
    else:
        w = 0
        while w < len(self.data) and self.data[w] < k:
            w += 1
        self = node(data=self.data, next=self.next[:w] +
                 (erase(self.next[w], k),) + self.next[w + 1:])
        if len(self.next[w].data) < max_len // 2:
            assert len(self.next[w].data) == max_len // 2 - 1
            if w:
                if len(self.next[w - 1].data) == max_len // 2:
                    self = node(data=self.data, next=self.next[:w -1] +
                             (node(data=self.next[w -
                                               1].data +
                                   (self.data[w -
                                           1],) +
                                   self.next[w].data, next=self.next[w -
                                                                    1].next +
                                   self.next[w].next),) +
                             self.next[w:])
                    self = node(data=self.data[:w - 1] + self.data[w:],
                             next=self.next[:w] + self.next[w + 1:])
                else:
                    self = node(data=self.data,
                             next=self.next[:w] + (node(data=(self.data[w - 1],) + self.next[w].data,
                                                     next=(self.next[w - 1].next[-1],) + self.next[w].next),) + self.next[w + 1:])
                    self = node(
                        next=self.next, data=self.data[:w - 1] + (self.next[w - 1].data[-1],) + self.data[w:])
                    self = node(data=self.data,
                             next=self.next[:w - 1] + (node(data=self.next[w - 1].data[:-1],
                                                         next=self.next[w - 1].next[:-1]),) + self.next[w:])
            elif len(self.next[w + 1].data) == max_len // 2:
                self = node(data=self.data, next=self.next[:w] +
                         (node(data=self.next[w].data +
                               (self.data[w],) +
                               self.next[w +
                                      1].data, next=self.next[w].next +
                               self.next[w +
                                      1].next),) +
                         self.next[w +
                                1:])
                self = node(data=self.data[:w] + self.data[w + 1:],
                         next=self.next[:w + 1] + self.next[w + 2:])
            else:
                self = node(data=self.data,
                         next=self.next[:w] + (node(data=self.next[w].data + (self.data[w],),
                                                 next=self.next[w].next + (self.next[w + 1].next[0],)),) + self.next[w + 1:])
                self = node(next=self.next,
                         data=self.data[:w] + (self.next[w + 1].data[0],) + self.data[w + 1:])
                self = node(data=self.data,
                         next=self.next[:w + 1] + (node(data=self.next[w + 1].data[1:],
                                                     next=self.next[w + 1].next[1:]),) + self.next[w + 2:])
    return self

def to_list(self: node[T], l: list[T]) -> list[T]:
    if self.next[0] is None:
        for w in self.data:
            l.append(w)
    else:
        to_list(self.next[0], l)
        for w in range(len(self.data)):
            l.append(self.data[w])
            to_list(self.next[w + 1], l)
    return l


def chval(self: node[T], a, t, d, n) -> node[T]:
    if n:
        v = a[n][1]
        self = node(data=self.data,
                    next=self.next[:v] + (chval(self.next[v],
                                                    a,
                                                    t,
                                                    d,
                                                    n - 1),) + self.next[v + 1:])
    else:
        self = node(next=self.next,
                    data=self.data[:t] + (d,
                                                ) + self.data[t + 1:])
    return self


class b:

    def __init__(self, s=None):
        self.s = None
        if s is not None:
            self.s = get(s).decode()

    # def check(self):
    #     return
    #     if self.s is not None:
    #         check(self.s)

    def add(self, v):
        r = loads((self.s)) if self.s is not None else self.s
        q = node(data=[], next=[r])
        q = insert(q, v)
        r = q
        if not r.data:
            r = r.next[0]
        # r = upd(r)
        self.s = r
        # self.s=(dumps(r)) if r!=None else r

    def find(self, v):
        r = loads((self.s)) if self.s is not None else self.s
        if r is None:
            return []
        f = find(r, v)
        if f is None:
            return []
        f = f[0][0]
        return [f.data[f.data.index(v)]]

    def remove(self, v):
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

    # def __repr__(self):
    #     r = loads((self.s)) if self.s is not None else self.s
    #     return ''

    def to_list(self) -> list:
        r = loads((self.s)) if self.s is not None else self.s
        if r is None:
            return []
        return to_list(r, [])

    def getstr(self, d=0):
        self.s = upd(self.s)
        if d == 0:
            return put(self.s.encode(), m=1) if self.s is not None else self.s

    def __del__(self):
        self.getstr(d=1)


@functools.total_ordering
class item:

    def __init__(self, k, v=None):
        if isinstance(k, item):
            k, v = k.k, k.v
        self.k = k
        self.v = v

    def __lt__(self, o):
        return self.k < o.k

    def __eq__(self, o):
        return self.k == o.k

    # def __repr__(self):
    #     return 'item' + repr([self.k, self.v])

    def to_list(self):
        return [self.k, self.v]


class d:

    def __init__(self, s=None):
        self.b = b(s)

    def __getitem__(self, k):
        return self.b.find(item(k))[0].v

    def __setitem__(self, k, v):
        self.b.add(item(k, (v)))

    def __delitem__(self, k):
        self.b.remove(item(k))

    # def __repr__(self):
    #     return repr(self.b)

    def __contains__(self, k) -> bool:
        return bool(self.b.find(item(k)))

    def to_dict(self) -> dict:
        r = self.b.to_list()
        r = [w.to_list() for w in r]
        return dict(r)

    def getstr(self) -> str | None:
        return self.b.getstr()


if __name__ == '__main__':

    to_sleep = 0.0

    db_data = {}

    def put(file, m=16):
        time.sleep(to_sleep)
        k = ''
        while not k or k in db_data:
            k = ''.join(
                [
                    chr(
                        random.randint(32, 126)
                    ) for w in range(
                        random.randint(128, 1024)
                    )
                ]
            )
        db_data[k] = file
        return k

    def get(a, f=None):
        time.sleep(to_sleep)
        return db_data[a]

    s_s = b()
    sed = random.randint(-9999, 9999)
    sed=6543
    print(sed)
    random.seed(sed)
    a_s = set()
    # for w in range(99):
    #     q = random.choice([0] * 3 + [1] + [2])
    #     if q == 0:
    #         r = random.randint(-9999, 9999)
    #         a_s.add(r)
    #         s_s.add(r)
    #     if q == 1:
    #         r = random.choice(list(a_s)) if a_s and random.randint(
    #             0, -1 + 2) else random.randint(0, -1 + 9)
    #         assert (r in a_s) == bool(s_s.find(r))
    #         assert r not in a_s or s_s.find(r)[0] == r
    #     if q == 2 and a_s:
    #         r = random.choice(list(a_s))
    #         a_s.remove(r)
    #         s_s.remove(r)
    #     f = set(s_s.to_list())
    #     assert a_s == f
    # del a_s
    # a_d: dict[int, int] = dict()
    # s_d = d()
    # for w in range(99):
    #     q = random.choice([0] * 3 + [1] + [2] + [3])
    #     if q == 0:
    #         k = random.choice(list(a_d)) if a_d and random.randint(
    #             0, 1) else random.randint(-9999, 9999)
    #         v = random.randint(-9999, 9999)
    #         a_d[k] = v
    #         s_d[k] = v
    #     if q == 1:
    #         k = random.choice(list(a_d)) if a_d and random.randint(
    #             0, 1) else random.randint(-9999, 9999)
    #         assert (k in a_d) == (k in s_d)
    #     if q == 2 and a_d:
    #         k = random.choice(list(a_d))
    #         a_d[k] == s_d[k]
    #     if q == 3 and a_d:
    #         k = random.choice(list(a_d))
    #         del a_d[k]
    #         del s_d[k]
    #     assert s_d.to_dict() == a_d
    #     s_d = d(s_d.getstr())

    a_d = dict()
    s_d = d()
    for w in range(4):
        k = random.randint(-9999, 9999)
        v = random.randint(-9999, 9999)
        s_d[k] = v
        a_d[k] = v

        treeprint(s_d.b.s)

        assert s_d.to_dict() == a_d
        s_d = d(s_d.getstr())

    for w in range(4):
        k = random.choice(list(a_d))
        del a_d[k]
        del s_d[k]

        treeprint(s_d.b.s)

        assert s_d.to_dict() == a_d
        s_d = d(s_d.getstr())

    to_sleep = 0.01
    for w in range(19):
        q = random.choice([0] + [1] + [2] + [3])
        if q == 0:
            k = random.choice(list(a_d)) if a_d and random.randint(
                0, 1) else random.randint(-9999, 9999)
            v = random.randint(-9999, 9999)
            a_d[k] = v
            s_d[k] = v
        if q == 1:
            k = random.choice(list(a_d)) if a_d and random.randint(
                0, 1) else random.randint(-9999, 9999)
            assert (k in a_d) == (k in s_d)
        if q == 2 and a_d:
            k = random.choice(list(a_d))
            a_d[k] == s_d[k]
        if q == 3 and a_d:
            k = random.choice(list(a_d))
            del a_d[k]
            del s_d[k]
