

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
from tkinter import *
from io import BytesIO
from os.path import getsize
from os import remove

def api(path, data=''):
	if path and path[-1] not in '&?':
		if '?' in path:
			path += '&'
		else:
			path += '?'
	sleep(1 / 6)
	data = data.encode()
	ret = loads(
		urlopen(
			'https://api.vk.com/method/' +
			path +
			'v=5.101&access_token=' +
			cred['token'],
			data=data).read().decode())
	try:
		return ret['response']
	except BaseException:
		print(ret)

def upload_short_data(data):
	name = str(time()) + '.txt'
	data=BytesIO(data)
	url = api(f'''docs.getMessagesUploadServer?peer_id={cred['aid']}''')['upload_url']
	r = post(url,files={'file': (name, data)}).json()
	url = api('docs.save?file=' + r['file'] + '&title=' + name)['doc']['url']
	return url

def download_short_data(link):
	return bytearray(urlopen(link).read())

def upload_data(rstream,size):
	link=''
	while size>0:
		data=bytearray()+link.encode()+chr(0).encode()
		toread=min([2000000-len(data),size])
		data+=rstream.read(toread)
		size-=toread
		link=upload_short_data(data)
	return link

def download_data(link,wstream=BytesIO()):
	rwcache=str(Path.home())+'/.vkcloud.cache.tmp'
	rwstream=open(rwcache,'wb')
	rwsize=0
	while link!='':
		data=download_short_data(link).split(bytearray(chr(0).encode()),1)
		link=data[0].decode()
		rwstream.write(data[1][::-1])
		rwsize+=len(data[1][::-1])
	rwstream=open(rwcache,'rb')
	for w in range(rwsize):
		rwstream.seek(rwsize-1-w)
		wstream.write(rwstream.read(1))
	remove(rwcache)
	return wstream



	if wstream.seekable():
		wstream.seek(0)
	return wstream


cred=dict()
cred['token']='354b4a71f66d4cb66b66918c073b3aff05e8743458c7ecaaea0ca3505e968fcff4564b618e988fde944e5'
cred['gid']='200708227'
cred['aid']='225847803'

download_data(upload_data(open('cloud.py','rb'),getsize('cloud.py')),open('cloud1','wb'))


'''
root = Tk()  
opt=Frame(root)
opt.place(heigth=128)
cont=Frame(root)
cont.place(x=128)
'''