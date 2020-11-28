

""":"
python3 $0 $@
exit
":"""

from pathlib import Path
from sys import argv
from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as fo
from requests import post
from http.server import BaseHTTPRequestHandler, HTTPServer
_____op = open
exec('from os import *')
exec('from os.path import *')
open = _____op


def api(path, data=''):
    if path and path[-1] not in '&?':
        if '?' in path:
            path += '&'
        else:
            path += '?'
    sleep(1 / 6)
    data = data.encode()
    global token
    ret = loads(
        urlopen(
            'https://api.vk.com/method/' +
            path +
            'v=5.101&access_token=' +
            token,
            data=data).read().decode())
    try:
        return ret['response']
    except BaseException:
        print(ret)


def log(p=None):
    if p is None:
        print(' ' * wid, end='\r')
    else:
        print('#' * int(p * wid), end='\r')


home = str(Path.home())
if home[-1] != '/':
    home += '/'

if not exists(home + '.cloud.token'):
    group = dict()
    token = input('''
select group or create one. You should be creator of group.
allow messages to group and write a random message to group from your account
create API token with acess to docs and messages and enter: ''')
    group['token'] = token
    group['gid'] = None
    group['cid'] = None
    if api('messages.getConversations') is not None:
        open(home + '.cloud.token', 'w').write(dumps(group))
    else:
        print('error: invalid token')
        exit()
group = loads(open(home + '.cloud.token').read())
token = group['token']
gid = group['gid']
cid = group['cid']

try:
    wid = get_terminal_size()[0]
except BaseException:
    wid = 0

if cid is None or gid is None:
    mes = api('messages.getConversations')['items']
    while mes == []:
        print('send a random message to group from your account')
        mes = api('messages.getConversations')['items']
    mes = [w['conversation']['peer']['id'] for w in mes]
    mes = [[w] for w in mes]
    for w in mes:
        w[0] = api(f'docs.getMessagesUploadServer?peer_id={w[0]}')[
            'upload_url']
        log(mes.index(w) / len(mes))
    log()
    mes = [w[0] for w in mes]
    mes = [w for w in mes if w]
    mes = [w.split('?', 1)[1].split('&') for w in mes]
    mes = [[e.split('=') for e in w] for w in mes]
    mes = [dict(w) for w in mes]
    d = dict()
    for e in mes[0].keys():
        if all([e in w and w[e] == mes[0][e] for w in mes]):
            d[e] = mes[0][e]
    for w in list(d.keys()):
        try:
            int(d[w])
        except BaseException:
            del(d[w])
    d = [d[w] for w in d if'id' in w and d[w][0] == '-']
    d = max(d, key=len)
    gid = str(abs(int(d)))
    mem = api(f'groups.getMembers?group_id={gid}&filter=managers')['items']
    mem = [w['id'] for w in mem if w['role'] == 'creator']
    cid = str(mem[0])
    group['gid'] = gid
    group['cid'] = cid
    open(home + '.cloud.token', 'w').write(dumps(group))


def post_data(data):
    name = str(time()) + '.txt'
    open(home + '.cloud.tmp', 'wb').write(data)
    url = api(f'docs.getMessagesUploadServer?peer_id={cid}')['upload_url']
    r = post(
        url,
        files={
            'file': (
                name,
                open(
                    home +
                    '.cloud.tmp',
                    'rb'))}).json()
    url = api('docs.save?file=' + r['file'] + '&title=' + name)['doc']['url']
    return url


def load_data(link):
    return urlopen(link).read()


class textfile:
    def __init__(self, text=''):
        self.data = bytearray(text.encode())

    def size(self):
        return len(self.data)

    def read(self, n=None):
        if n is None:
            f = self.data
            self.data = bytearray()
            return f
        else:
            f = self.data[:n]
            self.data = self.data[n:]
            return f

    def write(self, data):
        self.data += bytearray(data)


def upload_file(file, size):
    aa = ''
    msize = 200000000
    osize = size
    while size > msize:
        aa += post_data(file.read(msize)) + ' '
        size -= msize
        log((osize - size) / osize)
    if size:
        aa += post_data(file.read(size)) + ' '
    log()
    return post_data(aa.encode())


def download_file(file, link):
    a = load_data(link)
    a = a.decode().split()
    for w in a:
        file.write(load_data(w))
        log(a.index(w) / len(a))
    log()
    return file


def load_db():
    global db
    try:
        db = loads(
            download_file(
                textfile(), api(
                    'storage.get?key=url&user_id=' + cid)).read().decode())
    except BaseException:
        db = dict()


load_db()
dbc = 0

while (len(argv) < 2 or argv[1] not in ['list', 'upload', 'download', 'rename', 'exit']):
    argv += ['']
    print(f'''
usage: {argv[0]} upload FILE
       {argv[0]} download FILE
       {argv[0]} list
       {argv[0]} rename OLD_FILE_NAME NEW_FILE_NAME
       {argv[0]} exit
''')
    open(home + '.cloud.py', 'w').write('''
from sys import argv
from json import dumps
print(dumps(argv))
''')
    argv0 = argv[0]
    argv = loads(
        popen(
            'python3 ' +
            home +
            '.cloud.py ' +
            input('enter command: ')).read())
    argv[0] = argv0


if argv[1] == 'upload':
    if len(argv) < 3:
        print('usage: ' + argv[0] + ' upload FILE')
    elif not exists(argv[2]):
        print('error: name ' + argv[2] + ' not found in local filesystem')
    elif argv[2] in db.keys():
        print('error: name ' + argv[2] + ' found in remote filesystem')
    else:
        dbc = 1
        db[abspath(argv[2]).split('/')[-1]
           ] = upload_file(open(argv[2], 'rb'), getsize(argv[2]))

if argv[1] == 'download':
    if len(argv) < 3:
        print('usage: ' + argv[0] + ' download FILE')
    elif exists(argv[2]):
        print('error: name ' + argv[2] + ' found in local filesystem')
    elif argv[2] not in db.keys():
        print('error: name ' + argv[2] + ' not found in remote filesystem')
    else:
        download_file(open(argv[2], 'wb'), db[argv[2]])

if argv[1] == 'list':
    for w in db.keys():
        print(w)

if argv[1] == 'rename':
    if len(argv) < 4:
        print('usage: ' + argv[0] + ' rename OLD_FILE_NAME NEW_FILE_NAME')
    if argv[2] not in db.keys():
        print('error: name ' + argv[2] + ' not found in remote filesystem')
    if exists(argv[3]):
        print('error: name ' + argv[3] + ' found in remote filesystem')
    else:
        dbc = 1
        db[argv[3]] = db[argv[2]]
        del(db[argv[2]])


def save_db():
    global db
    db = textfile(dumps(db))
    url = upload_file(db, db.size())
    api(f'storage.set?key=url&value={url}&user_id={cid}')


if dbc:
    save_db()
