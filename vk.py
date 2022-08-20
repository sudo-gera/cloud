import base64
import pathlib
import traceback
from typing import Any
import urllib.request
import time
import json
import requests
import random
import builtins

__all__ = [
    'short_put',
    'short_get',
    'db_max_size',
    'root_get',
    'root_set',
    'home']

home = str(pathlib.Path.home()) + '/'


def vk_db():
    group = json.loads(builtins.open(home + '.cloud.token').read())
    token = group['token']
    gid = group['gid']
    cid = group['cid']
    db_max_size = 100_000_000

    def api(path: str):
        if path and path[-1] not in '&?':
            if '?' in path:
                path += '&'
            else:
                path += '?'
        time.sleep(1 / 6)
        data: Any = path
        try:
            data = urllib.request.urlopen(
                'https://api.vk.com/method/' +
                path +
                'v=5.101&access_token=' +
                token,
            ).read()
            data = data.decode()
            data = json.loads(data)
            data = data['response']
        except Exception:
            print(data)
            print(traceback.format_exc())
        return data

    def put(data: bytes) -> str:
        assert isinstance(data, bytes)
        assert len(data) <= db_max_size
        data = bytearray(data)
        c = 0
        for w in range(len(data)):
            data[w] = data[w] * 19 % 256
        data.append(random.randint(0, 255))
        c += 1
        while True:
            name = str(time.time()) + '.txt'
            url = api(f'docs.getWallUploadServer?group_id={gid}')['upload_url']
            r = requests.post(url, files={'file': (name, data)}).json()
            url = api(
                'docs.save?file=' +
                r['file'] +
                '&title=' +
                name)['doc']['url']
            u = urllib.request.urlopen(url)
            i = 0
            while i < len(data):
                r = list(u.read(1))
                if r != [data[i]]:
                    for w in range(len(data)):
                        data[w] = data[w] * 19 % 256
                    data.append(random.randint(0, 255))
                    c += 1
                    break
                else:
                    i += 1
            else:
                r = list(u.read())
                if r != []:
                    for w in range(len(data)):
                        data[w] = data[w] * 19 % 256
                    data.append(random.randint(0, 255))
                    c += 1
                else:
                    if c < 16:
                        return hex(c)[2:] + url[len('https://'):]
                    else:
                        return '|' + hex(c)[2:] + '|' + url[len('https://'):]

    def get(link: str) -> bytes:
        c: str | int
        if link[0] == '|':
            link = link[1:]
            c = link[:link.index('|')]
            link = link[len(c) + 1:]
        else:
            c = link[0]
            link = link[1:]
        c = int(c, 16)
        link = 'https://' + link
        data = urllib.request.urlopen(link).read()
        data = (data)
        for w in range(len(data)):
            data[w] = data[w] * pow(27, c, 256) % 256
        return bytes(data[:len(data) - c])

    def root_set(root: str) -> None:
        root = base64.b64encode(root.encode()).decode()
        try:
            api(f'storage.set?user_id={cid}&key=root&value={root}')
        except Exception:
            print(traceback.format_exc())

    def root_get() -> str | None:
        try:
            root = api(f'storage.get?user_id={cid}&key=root')
            if root:
                return base64.b64decode(root.encode()).decode()
            else:
                return None
        except Exception:
            print(traceback.format_exc())
        return None

    return put, get, db_max_size, root_set, root_get


def local_db():
    db_max_size = 40

    def put(data: bytes) -> str:
        assert isinstance(data, bytes)
        assert len(data) <= db_max_size
        try:
            db = json.loads(
                builtins.open(
                    home + '.cloud.json',
                    encoding='utf-8').read())
        except Exception:
            db = {}
        k = ''
        while k == '' or k in db:
            k = ''.join(
                [
                    chr(
                        random.randint(32, 126)
                    ) for w in range(
                        random.randint(4, 6)
                    )
                ]
            )
        db[k] = base64.b64encode(data).decode()
        builtins.open(home + '.cloud.json', 'w',
                      encoding='utf-8').write(json.dumps(db))
        return k

    def get(key: str) -> bytes:
        db = json.loads(builtins.open(home + '.cloud.json').read())
        return base64.b64decode(db[key].encode())

    def root_set(root: str) -> None:
        try:
            db = json.loads(
                builtins.open(
                    home + '.cloud.json',
                    encoding='utf-8').read())
        except Exception:
            db = {}
        db[''] = root
        builtins.open(home + '.cloud.json', 'w',
                      encoding='utf-8').write(json.dumps(db))

    def root_get() -> str | None:
        try:
            db = json.loads(
                builtins.open(
                    home + '.cloud.json',
                    encoding='utf-8').read())
        except Exception:
            db = {}
        if '' in db:
            return db['']
        return None

    return put, get, db_max_size, root_set, root_get


short_put, short_get, db_max_size, root_set, root_get = local_db()
# short_put,short_get,db_max_size,root_set,root_get=vk_db()
