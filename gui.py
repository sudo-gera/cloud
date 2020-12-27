

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
from urllib.parse import unquote
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
from functools import partial
from re import findall

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

def cast(part,arr,short):
	part,arr,short=part[:],arr[:],short[:]
	part=[w+1 for w in part]
	p=0
	for w in range(len(part)):
		p+=len(arr)**w*part[w]
	part=[]
	while p:
		part.append(p%len(short))
		p//=len(short)
	for w in range(len(part)-1):
		if part[w]<=0:
			part[w]+=len(short)
			part[w+1]-=1
	if part[-1]==0:
		part=part[:-1]
	part=[w-1 for w in part]

def partdumps(part,arr):
	short=[chr(w) for w in range(256) if len(dumps(w))==3]
	part=[arr.index(w) for w in part]
	part=cast(part,arr,short)
	part=[short[w] for w in part]
	return ''.join(part)


def linkdumps(link):
	a=findall(r'^https://vk\.com/doc([0-9]*)_([0-9]*)\?hash=([0-9a-f]*)&dl=FUZDAMBXGA4DEMRX:1606672057:([0-9a-f]*)&api=1&no_preview=1$',link)
	if len(a)!=1:
		return link
	a=list(a[0])
	a[0]=partdumps(a[0],'0123456789')
	a[1]=partdumps(a[1],'0123456789')
	a[2]=partdumps(a[2],'0123456789abcdef')
	a[3]=partdumps(a[3],'0123456789abcdef')
	a='\t'.join(a)
	return a

def partloads(part,short):
	arr=[chr(w) for w in range(256) if len(dumps(w))==3]
	part=[arr.index(w) for w in part]
	part=cast(part,arr,short)
	part=[short[w] for w in part]
	return ''.join(part)
	
def linkloads(link):
	if '\t' not in link:
		return link
	a=link.split('\t')
	a[0]=partloads(a[0],'0123456789')
	a[1]=partloads(a[1],'0123456789')
	a[2]=partloads(a[2],'0123456789abcdef')
	a[3]=partloads(a[3],'0123456789abcdef')
	link='https://vk.com/doc'+a[0]+'_'+a[1]+'?hash='+a[2]+'&dl=FUZDAMBXGA4DEMRX:1606672057:'+a[3]+'&api=1&no_preview=1'
	return link

def upload_short_data(data):
	name = str(time()) + '.txt'
	data=BytesIO(data)
	url = api(f'''docs.getMessagesUploadServer?peer_id={cred['cid']}''')['upload_url']
	r = post(url,files={'file': (name, data)}).json()
	url = api('docs.save?file=' + r['file'] + '&title=' + name)['doc']['url']
	url=linkdumps(url)
	return url

def download_short_data(link):
	link=linkloads(link)
	return bytearray(urlopen(link).read())

def upload_data(rstream,size=None):
	if size==None:
		wstream=BytesIO()
		data=rstream.read()
		size=len(data)
		wstream.write(data)
		wstream.seek(0)
		rstream=wstream
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

def dictsget():
	links=download_data(api('storage.get?key=dicts&user_id=' + cred['cid'])).read().decode()
	links=[loads('['+w+']') for w in links.split('\n')]
	links=dict(links)
	return links

def dictsset(links):
	links=[dumps([w,links[w]])[1:-1] for w in links]
	links='\n'.join(links)
	api('storage.set?key=dicts&value='+quote(upload_data(BytesIO(links.encode())))+'&user_id=' + cred['cid'])


def dictget(key):
	links=dictsget()
	if key in links.keys():
		return links[key]

def dictset(key,val):
	links=dictsget()
	links[key]=val
	dictsset(links)

def dictdel(key):
	links=dictsget()
	if key in links.keys():
		del(links[key])
		dictsset(links)

def download(key,wstream=BytesIO()):
	return download_data(dictget(key),wstream)

def upload(key,rstream,size=None):
	dictset(key,upload_data(rstream,size))
	return key

cred=dict()
cred['token']='354b4a71f66d4cb66b66918c073b3aff05e8743458c7ecaaea0ca3505e968fcff4564b618e988fde944e5'
cred['gid']='200708227'
cred['cid']='225847803'

def clear(w):
	for e in 'slaves place_slaves pack_slaves grid_slaves'.split():
		for q in eval('w.'+e+'()'):
			q.destroy()

def dirview(link):
	clear(root)
	global path
	json=download_data(link).read().decode()
	opt=Frame(root,height=128)
	opt.grid(column=0,row=0)
	Label(text=path)
	scr=Listbox(d)
	scr.grid(column=0,row=2)
	json=[loads(w) for w in json.split('\n')]
	Button(opt,text='back').grid(column=0,row=0)
	Button(opt,text='new dir').grid(column=1,row=0)
	Button(opt,text='download').grid(column=2,row=0)
	Button(opt,text='upload dir').grid(column=3,row=0)
	Button(opt,text='upload file').grid(column=4,row=0)
	scr.insert(Button(scr,text='download this dir'))
	for w in json:
		if w['type']=='dir':
			src.insert(Button(scr,text=w['name'],command=partial(dirview,w['link'])))
		if w['type']=='file':
			src.insert(Button(scr,text=w['name'],command=partial(fileview,w['link'])))

def fileview(link):
	pass

def showinfo(json):
	pass

def ren():
	pass

def rem():
	pass

def mov():
	pass

def cop():
	pass

def upl():
	pass

def loginpage():
	clear(root)
	Label(root,text="enter login").grid(column=0,row=0)
	Entry(root).grid(column=0,row=1)
	Button(root,text='enter').grid(column=0,row=2)

def page(root):
	pass


if __name__ == '__main__':
	path='/'
	root = Tk()
#	api('storage.get?key=root&user_id=' + cred['cid'])
	root.mainloop()

