from kivy.app import App
from urllib.request import urlopen
from json import loads
from json import dumps
from time import sleep
from time import time
from requests import post
from io import BytesIO as io
_____op = open
exec('from os import *')
exec('from os.path import *')
open = _____op
rename_=rename

class _kg:
	def __getattr__(s, n):
		for w in [ 'uix.','storage.','']:
			try:
				exec('from kivy.' + w + n.lower() + ' import ' + n)
				return eval(n)
			except:
				pass

get = _kg()

def log(q):
	q=str(q)
	b=get.BoxLayout(orientation='vertical')
	l=get.Popup(title='',content=b)
	b.add_widget(get.Label(text=q))
	b.add_widget(get.Button(text='close',on_release=l.dismiss))
	l.open()

def loading(q=None):
	global lo
	if q==None:
		try:
			lo.dismiss()
		except:
			pass
	else:
		q=str(q)
		lo=get.Popup(title='please wait',content=get.Label(text=q),auto_dismiss=False)
		lo.open()

def items(q):
	if type(q) == type(dict()):
		if set(q.keys()) == set(['count', 'items']):
			return items(q['items'])
		else:
			for w in q:
				q[w] = items(q[w])
			return q
	elif type(q) == type(list()):
		return [items(w) for w in q]
	else:
		return q

def api(path, data=''):
	if path and path[-1] not in '&?':
		if '?' in path:
			path += '&'
		else:
			path += '?'
	sleep(1 / 6)
	data = data.encode()
	global token
	try:
		ret = loads(
			urlopen(
				'https://api.vk.com/method/' +
				path +
				'v=5.101&access_token=' +
				token,
				data=data).read().decode())
	except:
		log('no internet connection')
		return
	try:
		return items(ret['response'])
	except:
		log(ret)

def load_cred():
	ore=get.JsonStore('credentials.json')
	global token,gid,cid
	token=gid=cid=None
	try:
		d=ore.get('cred')
		token=d['token']
		gid=d['gid']
		cid=d['cid']
	except:
		pass

def save_cred():
	ore=get.JsonStore('credentials.json')
	global token,gid,cid
	try:
		d=dict()
		ore.put('cred',token=token,gid=gid,cid=cid)
	except:
		pass


def load_db():
	global db
	db = dict()
	try:
		db = loads(download_file(textfile(), api('storage.get?key=url&user_id=' + cid)).read().decode())
	except:
		pass
	return db

def post_data(data):
	name = str(time()) + '.txt'
	f=io(data)
	url = api(f'docs.getMessagesUploadServer?peer_id={cid}')['upload_url']
	r = post(url,files={'file': (name,f)}).json()
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
	aa = ' '
	msize = 200000000
	osize = size
	while size > msize:
		aa += post_data(file.read(msize)) + ' '
		size -= msize
	if size:
		aa += post_data(file.read(size)) + ' '
	return post_data(aa.encode())

def download_file(file, link):
	a = load_data(link)
	a = a.decode().split()
	for w in a:
		file.write(load_data(w))
	return file

def check_token(instance):
	loading('checking token, wait please')
	global token,cid,gid
	token = instance.text
	a=api('messages.getConversations')
	if a!=None:
		save_cred()
		get_id()
		normal()
	else:
		pass
	loading()

def get_id():
	try:
		group = dict()
		global token,gid,cid
		group['token'] = token
		mes = api('messages.getConversations?count=1')
		while mes == []:
			log('send a random message to your group')
			mes = api('messages.getConversations?count=1')
		mes=mes[0]
		mes=mes['conversation']['peer']['id']
		mes = api(f'docs.getMessagesUploadServer?peer_id={mes}')['upload_url']
		mes = mes.split('?', 1)[1].split('&')
		mes = [e.split('=') for e in mes]
		mes = dict(mes)
		d=mes['mid']
		gid = str(abs(int(d)))
		mem = api(f'groups.getMembers?group_id={gid}&filter=managers')
		mem = [w['id'] for w in mem if w['role'] == 'creator']
		cid = str(mem[0])
		group['gid'] = gid
		group['cid'] = cid
		save_cred()
	except:
		log('system error')

def no_token(instance=None):
	global bg
	bg.clear_widgets()
	bg.add_widget(get.Label(text='Create new group in vk.com.\n'+
		'We recommend you to create new one instead of using old one.\n'+
		'You should be creator of group.\n'+
		'Allow messages to group and write a random message to group from your account.\n'+
		'Go to group settings and create API token with acess to docs and messages and enter'))
	t=get.TextInput(multiline=False)
	t.bind(on_text_validate=check_token)
	bg.add_widget(t)

def listing(a,r):
	global files
	files.clear_widgets()
	c=0
	for w in a:
		if c%9==0:
			p=get.BoxLayout(orientation='vertical')
			files.add_widget(p)
		b=get.Button(text=w[:80])
		b.filename=w
		b.frompage=r
		b.bind(on_release=file)
		p.add_widget(b)
		c+=1

def local(instance=None):
	global fg,files
	fg.clear_widgets()
	files=get.PageLayout()
	fg.add_widget(files)
	listing([w for w in listdir(sd1) if isfile(sd1+w)],'local')

def remote(instance=None):
	global fg,files
	fg.clear_widgets()
	files=get.PageLayout()
	fg.add_widget(files)
	load_db()
	global db
	listing(list(db.keys()),'remote')

def file(instance=None):
	global fg
	fg.clear_widgets()
	p=get.BoxLayout(orientation='vertical')
	p.add_widget(get.Label(text=instance.text))
	v=['local','remote']
	b=get.Button(text='copy to '+v[1-v.index(instance.frompage)])
	b.frompage=instance.frompage
	b.filename=instance.filename
	b.bind(on_release=copy)
	p.add_widget(b)
	b=get.Button(text='rename')
	b.frompage=instance.frompage
	b.filename=instance.text
	b.bind(on_release=rename)
	p.add_widget(b)
	fg.add_widget(p)

def copy(instance=None):
	load_db()
	global db
	if instance.frompage=='remote':
		if exists(sd1+instance.filename):
			log(instance.filename+' exists in local')
		else:
			try:
				loading('downloading '+instance.filename)
				download_file(open(sd1+instance.filename,'wb'),db[instance.filename])
			except:
				log('unable to download '+instance.filename)
			loading()
			normal()
	if instance.frompage=='local':
		if instance.filename in db:
			log(instance.filename+' exists in remote')
		else:
			try:
				loading('uploading '+instance.filename)
				db[instance.filename]=upload_file(open(sd1+instance.filename,'rb'),getsize(sd1+instance.filename))
			except:
				log('unable to upload '+instance.filename)
			loading()
			normal()
	save_db()

def rename(instance=None):
	global fg
	fg.clear_widgets()
	fg.add_widget(get.Label(text='new name'))
	t=get.TextInput(multiline=False)
	t.frompage=instance.frompage
	t.filename=instance.filename
	t.bind(on_text_validate=rename_file)
	fg.add_widget(t)

def rename_file(instance=None):
	for w in '|/ ()\t\n\\\"\'':
		instance.text.replace(w,'_')
	if instance.frompage=='remote':
		if instance.text in db.keys():
			log(instance.filename+' exists in remote')
		else:
			db[instance.text]=db[instance.filename]
			del(db[instance.filename])
			save_db()
			normal()
	if instance.frompage=='local':
		if exists(sd1+instance.text):
			log(instance.filename+' exists in local')
		else:
			rename_(sd1+instance.filename,sd1+instance.text)
			normal()



def logout(instance=None):
	global token,gid,cid
	token=cid=gid=None
	save_cred()
	no_token()

def save_db():
	global db
	db = textfile(dumps(db))
	try:
		url = upload_file(db, db.size())
	except:
		log('unable to save files info')
	api(f'storage.set?key=url&value={url}&user_id={cid}')

def normal(instance=None):
	global bg
	bg.clear_widgets()
	box1=get.BoxLayout(orientation='vertical')
	box2=get.BoxLayout(orientation='horizontal',size_hint=(1,.1))
	b=get.Button(text='local')
	b.bind(on_release=local)
	box2.add_widget(b)
	b=get.Button(text='remote')
	b.bind(on_release=remote)
	box2.add_widget(b)
	b=get.Button(text='logout')
	b.bind(on_release=logout)
	box2.add_widget(b)
	box1.add_widget(box2)
	global fg
	fg=get.GridLayout(cols=1,size_hint=(1,.9))
	box1.add_widget(fg)
	bg.add_widget(box1)

class vk_cloud(App):
	def build(self):
		global bg
		bg=get.GridLayout(cols=1)
		try:
			sd1='/storage/emulated/0/'
			app='/storage/emulated/0/'
#			from pathlib import Path
#			home=Path.home()
#			sd1=app=home
#			from android.permissions import request_permissions, Permission, check_permissions
#			perms=[Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE,Permission.INTERNET]
#			while  not check_permissions(perms):
#				log('needs all permissions')
#				request_permissions(perms)
		except:
			pass
		load_cred()
		global token,gid,cid
		_ret=normal
		if not token:
			_ret=no_token
		elif not cid or not gid:
			get_id()
		_ret()
		return bg

vk_cloud().run()
