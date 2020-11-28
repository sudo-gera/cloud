#from android.permissions import request_permissions, Permission, check_permissions
from functools import partial
from json import loads
from json import dumps
from io import BytesIO as io
from kivy.app import App
from kivy.lang import Builder
from urllib.parse import quote
from urllib.parse import unquote
from urllib.request import urlopen as ou
from plyer import *
from pprint import pprint
#from requests_toolbelt import MultipartEncoder
from time import sleep
from time import time
_____op = open
exec('from os import *')
exec('from os.path import *')
open = _____op
from kivy.clock import Clock
rename_=rename
for w in dir(Clock):
	if '_' not in [w[:1],w[-1:]]:
		exec(w+'=Clock.'+w)

class _kg:
	def __getattr__(s, n):
		for w in [ 'uix.','storage.','network.','']:
			try:
				exec('from kivy.' + w + n.lower() + ' import ' + n)
				return eval(n)
			except:
				pass

get = _kg()

def urlopen(url,data=None):
	d=get.UrlRequest(url,req_body=data,decode=False,on_error=partial(log,'no internet connection'))
	d.wait()
	r=d.result
	if type(r)==type(dict()):
		r=dumps(r)
	if type(r)==type(str()):
		r=r.encode()
	return r

def log(q):
	q=str(q)
	b=get.BoxLayout(orientation='vertical')
	l=get.Popup(title='',content=b)
	b.add_widget(get.Label(text=q))
	b.add_widget(get.Button(text='close',on_release=l.dismiss))
	l.open()
	notification.notify(message=q)

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
				data=data).decode())
	except:
		return
	try:
		return items(ret['response'])
	except:
		pass
	try:
		log(ret['error']['error_msg'])
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

def logprint(q):
	print([q])
	return q

def load_db():
	global db
	try:
		db = loads(download_file(textfile(), unquote(api('storage.get?key=url&user_id=' + cid))).read().decode())
	except:
		db=dict()
	return db

def post_data(data):
	name = str(time()) + '.txt'
	url = api(f'docs.getMessagesUploadServer?peer_id={cid}')['upload_url']
	payload=MultipartEncoder(fields={'file':(name,data,'text/plain')})
	headers={'Content-Type':payload.content_type}
	d=get.UrlRequest(url,req_headers=headers,req_body=payload,on_error=partial(log,'no internet connecton'))
	d.wait()
	r=d.result
	url = api('docs.save?file=' + r['file'] + '&title=' + name)['doc']['url']
	return url

def load_data(link):
	return ou(link).read()

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

	def __str__(self):
		return 'textfile: '+str(self.data)

def upload_file(file, size=None):
	aa = ' '
	msize = 200000000
	osize = size
	if size==None:
		file=file.read()
		size,file=len(file),io(file)
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

def check_token(*q,**w):
	global token,cid,gid
	token = root.children[1].text
	a=api('messages.getConversations')
	if a!=None:
		save_cred()
		get_id()
		listing()
	else:
		pass
	
def get_id():
	try:
		global token,gid,cid
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
		save_cred()
	except:
		log('system error')

def no_token(*q,**w):
	root.clear_widgets()
	root.add_widget(get.Label(text='Create new group in vk.com.\n'+
		'We recommend you to create new one instead of using old one.\n'+
		'You should be creator of group.\n'+
		'Allow messages to group and write a random message to group from your account.\n'+
		'Go to group settings and create API token with acess to docs and messages and enter:'))
	root.add_widget(get.TextInput(multiline=False,on_text_validate=check_token))
	root.add_widget(get.Button(text='check token',on_release=check_token))

Builder.load_string('''
<RV>:
    viewclass: 'Button'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


def button(q,w):
	return {'text':str(q),'on_release':partial(w,q)}

class RV(get.RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

def listing(*q,**w):
	root.clear_widgets()
	root.add_widget(box(orientation='horizontal',size_hint=(1,.1)))
	root.add_widget(get.Label(text='loading...'))
	load_db()
	root.children[1].add_widget(get.Button(text='logout',on_release=logout))
	root.children[1].add_widget(get.Button(text='upload',on_release=upload))
	root.children[1].add_widget(get.Button(text='refresh',on_release=listing))
	root.remove_widget(root.children[0])
	d=list(db.keys())
	if d:
		root.add_widget(RV())
		root.children[0].data=[button(w,file) for w in d]
	else:
		root.add_widget(get.Label(text='empty'))

def file(filename,*q,**w):
	root.clear_widgets()
	root.add_widget(get.Button(text='back',on_release=listing))
	root.add_widget(get.Label(text=filename))
	root.add_widget(get.Button(text='download',on_release=partial(download,filename)))
	root.add_widget(get.Button(text='rename',on_release=partial(rename,filename)))

def upload(*q,**w):
	q=filechooser.open_file(multiple=True,title='upload files...')
	for w in q:
		w=split(w)[1]
		load_db()
		if w in db.keys():
			log('name '+w+' is used')
			continue
		try:
			f=open(w,'rb')
		except:
			log('file '+w+' is unreadable')
			continue
		try:
			s=getsize(w)
		except:
			s=None
		try:
			db[w]=upload_file(f,s)
			save_db()
			listing()
		except:
			log('unable to upload file '+q)

def download(filename,*q,**w):
	q=filechooser.save_file(title='download to...',path=filename)
	for w in q:
		load_db()
		try:
			f=open(w,'wb')
		except:
			log('file '+w+' is unreadable')
			continue
		try:
			download_file(f,db[filename])
		except:
			log('unable to download file '+q)

def rename(filename,*q,**w):
	root.clear_widgets()
	root.add_widget(get.Button(text='back',on_release=listing))
	root.add_widget(get.Label(text='new name'))
	root.add_widget(get.TextInput(text=filename,multiline=False,on_text_validate=partial(rename_file,filename)))
	root.add_widget(get.Button(text='rename',on_release=partial(rename_file,filename)))

def rename_file(filename,*q,**w):
	load_db()
	name=root.children[1].text
	for w in '|/ ()\t\n\\\"\'':
		name.replace(w,'_')
	if name=='':
		log('name is too short')
		return
	if name in db.keys():
		log('name '+name+' is already used')
		return
	db[name]=db[filename]
	del(db[filename])
	save_db()
	listing()


def logout(instance=None):
	global token,gid,cid
	token=cid=gid=None
	save_cred()
	no_token()

def save_db():
	global db
	db = textfile(dumps(db))
	try:
		url = upload_file(db)
		d=api(f'storage.set?key=url&value={quote(url)}&user_id={cid}')
		if d!=1:
			raise BaseException
	except:
		log('unable to save files info')


box=get.BoxLayout

class vk_cloud(App):
	def build(self):
		global root
		root=box(orientation='vertical')
		try:
			perms=[Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE,Permission.INTERNET]
			while not check_permissions(perms):
				log('needs all permissions')
				request_permissions(perms)
		except:
			pass
		load_cred()
		global token,gid,cid
		if not token:
			get.Clock.schedule_once(no_token)
		else:
			if not cid or not gid:
				get_id()
			get.Clock.schedule_once(listing)
		return root

vk_cloud().run()
