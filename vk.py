from base64 import b64decode, b64encode
from pathlib import Path
from traceback import format_exc
from urllib.request import urlopen
import time
import json
post=__import__('requests').post
import random
from builtins import open

home = str(Path.home())
if home[-1] != '/':
    home += '/'

def api(path):
    if path and path[-1] not in '&?':
        if '?' in path:
            path += '&'
        else:
            path += '?'
    time.sleep(1 / 6)
    global token
    u=path
    try:
        u=urlopen(
                'https://api.vk.com/method/' +
                path +
                'v=5.101&access_token=' +
                token,
            ).read()
        u=u.decode()
        u=json.loads(u)
        u=u['response']
    except Exception:
        print(u)
        print(format_exc())
    return u

group = json.loads(open(home + '.cloud.token').read())
token = group['token']
gid = group['gid']
cid = group['cid']

def vk_db():
    db_max_size=100_000_000
    def put(data):
        data=bytearray(data)
        assert type(data) in [bytes,bytearray]
        assert len(data)<=db_max_size
        c=0
        while 1:
            name = str(time.time()) + '.txt'
            url = api(f'docs.getWallUploadServer?group_id={gid}')['upload_url']
            r = post(url,files={'file': (name,data)}).json()
            url = api('docs.save?file=' + r['file'] + '&title=' + name)['doc']['url']
            u=urlopen(url)
            i=0
            while i<len(data):
                r=list(u.read(1))
                if r!=[data[i]]:
                    for w in range(len(data)):
                        data[w]=data[w]*19%256
                    data.append(random.randint(0,255))
                    c+=1
                    break
                else:
                    i+=1
            else:
                r=list(u.read())
                if r!=[]:
                    for w in range(len(data)):
                        data[w]=data[w]*19%256
                    data.append(random.randint(0,255))
                    c+=1
                else:
                    if c<16:
                        return hex(c)[2:]+url[len('https://'):]
                    else:
                        return '|'+hex(c)[2:]+'|'+url[len('https://'):]

    def get(link):
        if link[0]=='|':
            link=link[1:]
            c=link[:link.index('|')]
            link=link[len(c)+1:]
        else:
            c=link[0]
            link=link[1:]
        c=int(c,16)
        link='https://'+link
        data=urlopen(link).read()
        data=bytearray(data)
        for w in range(len(data)):
            data[w]=data[w]*pow(27,c,256)%256
        return data[:len(data)-c]

    return put,get,db_max_size

def local_db():
    db_max_size=40
    to_sleep=0.1
    def put(data):
        assert type(data) in [bytes,bytearray]
        assert len(data)<=db_max_size
        # time.sleep(to_sleep)
        # time.sleep(1.3623757362365723)
        try:
            db=json.loads(open(home+'.cloud.json',encoding='utf-8').read())
        except Exception:
            db={}
        k = ''
        while k=='' or k in db:
            k = ''.join(
                [
                    chr(
                        random.randint(32, 126)
                    ) for w in range(
                        random.randint(4, 6)
                    )
                ]
            )
        db[k] = b64encode(data).decode()
        open(home+'.cloud.json','w',encoding='utf-8').write(json.dumps(db))
        return k

    def get(key):
        # time.sleep(to_sleep)
        # time.sleep(0.22823095321655273)
        db=json.loads(open(home+'.cloud.json').read())
        return b64decode(db[key].encode())

    def root_set(root):
        try:
            db=json.loads(open(home+'.cloud.json',encoding='utf-8').read())
        except Exception:
            db={}
        db['']=root
        open(home+'.cloud.json','w',encoding='utf-8').write(json.dumps(db))

    def root_get():
        try:
            db=json.loads(open(home+'.cloud.json',encoding='utf-8').read())
        except Exception:
            db={}
        if '' in db:
            return db['']

    return put,get,db_max_size,root_set,root_get



short_put,short_get,db_max_size,root_set,root_get=local_db()
# short_put,short_get,db_max_size=vk_db()

__all__=['short_put','short_get','db_max_size','root_get','root_set']

