from b_mem import *
# from pathlib import Path
import json
import os
import os.path
import time

# def normalpath(p):
#     p = p.replace('\\', '/')
#     p = p.split('/')
#     p = [w for w in p if w]
#     p = '/'.join(p)
#     p = '/' + p
#     return p


# class filesystem:
#     def __init__(self):
#         self.root=d(root_get())
#     def 

def json_file(**d):
    assert 'type' in d
    assert 'cont' in d
    if d['type']=='file':
        assert 'size' in d
    return d


files:b_dict[int|url]=b_dict(root_get())

if 0 not in files:
    files[0]=json_file(
        type='file',
        cont=''
    )

class path:
    def __init__(self,p:str)->None:
        p = p.replace('\\', '/')
        pl = p.split('/')
        pl = [w for w in pl if w]
        p = '/'.join(pl)
        self.p=p
    def __str__(self)->str:
        return '/'+self.p
    def open(self):
        


# @typechecked
# def mkdir(p:path)->None:


class directory:
    def __init__(self,p:path):
        self.fd=p.open()
        self.d=b_dict(files[self.fd])
    def __getitem__(self,key):
        return self.d[key]
    def __setitem__(self,key,val):
        self.d[key]=val
    def __delitem__(self,key):
        del self.d[key]






# class directory:
#     def __init__(self,*,val=url()):
#         if type(val)==url:
#             self.content=d(val)
#             self.key=val
#         elif type(val)==d:
#             self.content=val
#             self.key=None
#     def __getitem__(self,k):
#         return self.content[k]
#     def __setitem__(self,k,v):
#         self.content[k]=v
#         self.key=None
#     def __detitem__(self,k):
#         del self.content[k]
#         self.key=None
#     def getstr(self):
#         return self.content.getstr()
#     def to_dict(self):
#         return self.content.to_dict()


# class filesystem:
#     def __init__(self):
#         self.root=d(root_get())
        

#         self.fs=d(root_get())
#         if '/' not in self.fs:
#             self.fs['/'] = {
#                 'size': 0,
#                 'date_created': time.time(),
#                 'date_modifed': time.time(),
#                 'type': 'dir',
#                 'cont': None
#             }
#     def __getitem__(self,n):
#         return self.fs[n]
#     def __delitem__(self,n):
#         del self.fs[n]
#     def __setitem__(self,n,v):
#         self.fs[n]=v
#     def __contains__(self,n):
#         return n in self.fs
#     def getstr(self):
#         return self.fs.getstr()
#     def setstr(self,s):
#         self.fs=d(s)
#     def sync(self):
#         if type(self.fs.b.s)!=str:
#             root_set(self.getstr())
#     def __del__(self):
#         if type(self.fs.b.s)!=str:
#             print('error: not synced')



# fs = d()
# fs={}

# class filesystem:
#     def __init__(self):
#         self.fs=d(root_get())
#         if '/' not in self.fs:
#             self.fs['/'] = {
#                 'size': 0,
#                 'date_created': time.time(),
#                 'date_modifed': time.time(),
#                 'type': 'dir',
#                 'cont': load.put(json.dumps({}).encode())
#             }
#     def __getitem__(self,n):
#         return self.fs[n]
#     def __delitem__(self,n):
#         del self.fs[n]
#     def __setitem__(self,n,v):
#         self.fs[n]=v
#     def __contains__(self,n):
#         return n in self.fs
#     def getstr(self):
#         return self.fs.getstr()
#     def setstr(self,s):
#         self.fs=d(s)
#     def sync(self):
#         if type(self.fs.b.s)!=str:
#             root_set(self.getstr())
#     def __del__(self):
#         if type(self.fs.b.s)!=str:
#             print('error: not synced')

# fs=filesystem()

# # def init():
# #     if '/' not in fs:
# #         fs['/'] = {
# #             'size': 0,
# #             'date_created': time.time(),
# #             'date_modifed': time.time(),
# #             'type': 'dir',
# #             'cont': load.put(json.dumps({}).encode())
# #         }




# def mkfile(p, v, t='file'):
#     p = normalpath(p)
#     d = os.path.split(p)
#     if d[0] not in fs:
#         raise OSError(f'{d[0]} does not exist.')
#     g = fs[d[0]]
#     if g['type'] != 'dir':
#         raise OSError(f'{d[0]} is not a directory.')
#     f = load.get(g['cont'])
#     f = json.loads(f.decode())
#     if p in fs:
#         raise OSError(f'{p} exists.')
#     if d[1] in f:
#         raise OSError(f'{p} exists.')
#     s = len(v)
#     b = load.put(v)
#     j = {
#         'size': s,
#         'date_created': time.time(),
#         'date_modifed': time.time(),
#         'type': t,
#         'cont': b
#     }
#     fs[p] = j
#     f[d[1]] = j
#     g['cont'] = load.put(json.dumps(f).encode())
#     fs[d[0]] = g


# def mkdir(p):
#     p = normalpath(p)
#     mkfile(p, json.dumps({}).encode(), 'dir')


# def cat(p, t='file'):
#     p = normalpath(p)
#     if p not in fs:
#         raise OSError(f'{p} does not exist.')
#     f = fs[p]
#     if f['type'] != t:
#         raise OSError(f'{p} is not a {t}.')
#     g = load.get(f['cont'])
#     return g


# def ls(p):
#     p = normalpath(p)
#     a = cat(p, 'dir')
#     a = json.loads(a.decode())
#     for w in a:
#         del a[w]['cont']
#     return a


# def ftype(p):
#     p = normalpath(p)
#     if p not in fs:
#         return None
#     return fs[p]['type']


# def tree(p):
#     p = normalpath(p)
#     f = ftype(p)
#     r = []
#     if f is not None:
#         r += [p]
#     if f == 'dir':
#         l = ls(p)
#         for w in l:
#             r += tree(p + '/' + w)
#     return r


# def cpfile(p1, p2):
#     p1 = normalpath(p1)
#     p2 = normalpath(p2)
#     if p1==p2:
#         raise OSError(f'files are same.')
#     if p1 not in fs:
#         raise OSError(f'{p1} does not exist.')
#     j = fs[p1]
#     if j['type'] != 'file':
#         raise OSError(f'{p1} is not a file.')

#     d = os.path.split(p2)
#     if d[0] not in fs:
#         raise OSError(f'{d[0]} does not exist.')
#     g = fs[d[0]]
#     if g['type'] != 'dir':
#         raise OSError(f'{d[0]} is not a directory.')
#     f = load.get(g['cont'])
#     f = json.loads(f.decode())
#     if d[1] in f:
#         raise OSError(f'{p2} exists.')

#     fs[p2] = j
#     f[d[1]] = j
#     g['cont'] = load.put(json.dumps(f).encode())
#     fs[d[0]] = g


# def rmfile(p):
#     p = normalpath(p)
#     if p not in fs:
#         raise OSError(f'{p} does not exist.')
#     j = fs[p]
#     if j['type'] != 'file':
#         raise OSError(f'{p} is not a file.')
#     d = os.path.split(p)
#     if d[0] not in fs:
#         raise OSError(f'{d[0]} does not exist.')
#     g = fs[d[0]]
#     if g['type'] != 'dir':
#         raise OSError(f'{d[0]} is not a directory.')
#     f = load.get(g['cont'])
#     f = json.loads(f.decode())
#     if d[1] not in f:
#         raise OSError(f'{p} does not exist.')
#     del fs[p]
#     del f[d[1]]
#     g['cont'] = load.put(json.dumps(f).encode())
#     fs[d[0]] = g

# def mvfile(p1,p2):
#     p1 = normalpath(p1)
#     p2 = normalpath(p2)
#     cpfile(p1,p2)
#     rmfile(p1)

