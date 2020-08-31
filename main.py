from kivy.app import App
from urllib.request import urlopen
from json import loads
from json import dumps
from time import sleep
from time import time
from requests import post
from traceback import format_exc as error
_____op = open
exec('from os import *')
exec('from os.path import *')
open = _____op
rename_=rename

class _kg:
	def __getattr__(s, n):
		for w in ['', 'uix.']:
			try:
				exec('from kivy.' + w + n.lower() + ' import ' + n)
				return eval(n)
			except:
				pass


get = _kg()

try:
	from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path
	app = str(app_storage_path)
	sd1 = str(primary_external_storage_path)
	sd2 = str(secondary_external_storage_path)
	app += '/' if app[-1] != '/' else ''
	sd1 += '/' if sd1[-1] != '/' else ''
	sd2 += '/' if sd2[-1] != '/' else ''
except:
	from pathlib import Path
	home = str(Path.home())
	home += '/' if home[-1] != '/' else ''
	app = sd1 = sd2 = home


def request():
	from android.permissions import request_permissions, Permission
	request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
						 Permission.READ_EXTERNAL_STORAGE,
						 Permission.INTERNET])


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


token = ''


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
	except: log(ret)


def save_db():
	global db
	db = textfile(dumps(db))
	url = upload_file(db, db.size())
	try:
		api(f'storage.set?key=url&value={url}&user_id={cid}')
	except: log(error())

db=dict()

def load_db():
	global db
	db = dict()
	try:
		db = loads(
			download_file(
				textfile(), api(
					'storage.get?key=url&user_id=' + cid)).read().decode())
	except: log(error())


def post_data(data):
	name = str(time()) + '.txt'
	open(app + '.cloud.tmp', 'wb').write(data)
	url = api(f'docs.getMessagesUploadServer?peer_id={cid}')['upload_url']
	r = post(
		url,
		files={
			'file': (
				name,
				open(
					app +
					'.cloud.tmp',
					'rb'))}).json()
	open(app + '.cloud.tmp', 'w')
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


def black(self):
	self.background_color = (0, 0, 0, 1)


def check_token(instance):
	log('wait please')
	global token
	token = instance.text
	a=api('messages.getConversations')
	if a!=None:
		d = dict()
		d['token'] = token
		d['cid'] = None
		d['gid'] = None
		open(app + '.token', 'w').write(dumps(d))
		try:
			get_id()
			normal()
		except: log(error())
	else:
		log('checking token failed')


def log(q):
	w=''
	q=str(q)
	while q:
		w=q[:80]+'\n'
		q=q[80:]
	global llab
	llab.text += str(w)+'\n'
	llab.text = llab.text[-1024:]


def get_id():
	group = dict()
	global token
	group['token'] = token
	mes = api('messages.getConversations')
	while mes == []:
		log('send a random message to group from your account')
		mes = api('messages.getConversations?count=8')
	mes = [w['conversation']['peer']['id'] for w in mes]
	mes = [[w] for w in mes]
	for w in mes:
		w[0] = api(f'docs.getMessagesUploadServer?peer_id={w[0]}')[
			'upload_url']
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
	mem = api(f'groups.getMembers?group_id={gid}&filter=managers')
	mem = [w['id'] for w in mem if w['role'] == 'creator']
	cid = str(mem[0])
	group['gid'] = gid
	group['cid'] = cid
	open(app + '.token', 'w').write(dumps(group))

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
		w=w[:80]
		if c%9==0:
			p=get.BoxLayout(orientation='vertical')
			files.add_widget(p)
		b=get.Button(text=w)
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
	b.filename=instance.text
	b.bind(on_release=copy)
	p.add_widget(b)
	b=get.Button(text='rename')
	b.frompage=instance.frompage
	b.filename=instance.text
	b.bind(on_release=rename)
	p.add_widget(b)
	fg.add_widget(p)

def wait():
	global bg
	bg.clear_widgets()
	bg.add_widget(get.Label(text='wait please'))
	print('wait')

def copy(instance=None):
	load_db()
	global db
	if instance.frompage=='remote':
		if exists(sd1+instance.filename):
			log(instance.filename+' exists in local')
		else:
			download_file(open(sd1+instance.filename,'wb'),db[instance.filename])
			normal()
	if instance.frompage=='local':
		if instance.filename in db:
			log(instance.filename+' exists in remote')
		else:
			db[instance.filename]=upload_file(open(sd1+instance.filename,'rb'),getsize(sd1+instance.filename))
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
			log(instance.text+' exists in remote')
		else:
			db[instance.text]=db[instance.filename]
			del(db[instance.filename])
			normal()
		save_db()
	if instance.frompage=='local':
		if exists(sd1+instance.text):
			log(instance.text+' exists in local')
		else:
			rename_(sd1+instance.filename,sd1+instance.text)
			normal()



def logout(instance=None):
	remove(app+'.token')
	no_token()

fg=None

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

llab=None
bg=None

class vk_cloud(App):
	def build(self):
		global llab,bg
		root=get.PageLayout()
		bg=get.GridLayout(cols=1)
		llab=get.Button(text='')
		llab.background_color=(0,0,0,1)
		llab.bind(on_press=black)
		llab.bind(on_release=black)
		root.add_widget(bg)
		root.add_widget(llab)
		log('this is logging page')
		try:
			request()
		except: log(error())
		_ret=no_token
		try:
			d=loads(open(app+'.token').read())
			global token,gid,cid
			token=d['token']
			gid=d['gid']
			cid=d['cid']
			if not cid or not gid:
				get_id()
			_ret=normal
		except: log(error())
		_ret()
		return root

vk_cloud().run()
