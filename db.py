from textwrap import shorten
from vk import *
import io
import json
def _put(file,m=float('inf')):
    a=[]
    while (c:=file.read(db_max_size)):
        a.append(short_put(c))
    j=json.dumps(a).encode()
    if len(a)>16 or len(j)>=m:
        a=put(io.BytesIO(j))
        if type(a[0])==str:
            a=[1]+a
        else:
            a[0]+=1
    return a

def put(file,m=float('inf')):
    if type(file) in [bytes,bytearray]:
        file=io.BytesIO(file)
    return json.dumps(_put(file,m))

def get(a,f=None):
    file=f if f!=None else io.BytesIO()
    a=json.loads(a)
    if type(a[0])==int:
        c=a[0]
        a=a[1:]
        for w in range(c):
            a=json.loads(b''.join([short_get(w) for w in a]).decode())
    for w in a:
        file.write(short_get(w))
    return file if f!=None else [file.seek(0),file.read()][1]

__all__=['put','get','root_get','root_set']