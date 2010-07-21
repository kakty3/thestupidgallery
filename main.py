import web, os, admin, users
from urlparse import urlparse

ImagesOnPage = 10
ImagesDatabaseName = 'images'

#web.config.debug = False

def ret(a, b, c):
	if a:
		return b
	else:
		return c

class index:
	def GET(self):
		return render.index()

def validUrl(url):
	parsed = urlparse(url)
	if (parsed.scheme == 'http') and (parsed.path):
		ext = parsed.path.split('/')[-1].split('.')[-1]
		try:
			['jpg', 'jpeg', 'gif', 'png'].index(ext)
		except ValueError:
			return 0
		else:
			return 1
	else:
		return 0

class add:
	def GET(self):
		if session.loggedin:
			i = web.input()
			print i
			if not i:
				return render.add()
			try:
				name = i.t
				url = i.u
			except AttributeError:
				#print 'ololo'
				return 'Bad request'
			else:
				#return 'name=%s url=%s' % (name, url)
				if validUrl(url):
					print '=' * 30
					print 'name \"%s\"' % name
					if name:
						n = db.insert('images', url=url, name=name, public=1, user_id=session.user_id)
						return 'name: %s\nurl: %s\nstatus: %s' % (name, url, 'posted')
					else:
						return render.message("Error", "Trying to add picture without name", "try again", "/add")
				else:
					return render.message("Error", "Url is not valid", "try again", "/add")
		else:
			return "Please, login to add pictures"

	def POST(self):
		i = web.input()
		#print i
		try:
			i.public
		except:
			public = 0
		else:
			public = 1
		url = i.url
		name  = i.name
		print 'name \'%s\'' % name
		if validUrl(url):
			if name:
				n = db.insert('images', url=i.url, name=i.name, public=public, user_id=session.user_id)
				return render.message("Well done", "Picture was succesfully added")
			else:
				return render.message("Error", "Trying to add picture without name", "try again", "/add")
		else:
			return render.message("Error", "Url is not valid", "try again", "/add")

class login:
	def GET(self):
		if not session.loggedin:
			return render.login()
		else:
			return render.message("Warning", "You are allready logged in")

	def POST(self):
		feedback = users.login(web.input())
		if feedback == 0:
			return render.message("Well done", "You were successfully loged in")
		else:
			return render.message("Error", feedback)#, 'try to login again', '/login')

class register:
	def GET(self):
		if not session.loggedin:
			return render.register()
		else:
			return render.message("Warning", "Please, log out to register")#, 'try to login again', '/login')

	def POST(self):
		i = web.input()
		print i
		if users.addUser(i.username, i.password):
			return render.message("Error", "Can't register", 'try again', '/register')
		return render.message("Welcome", "Your registration is succesful")

class test:
	def GET(self):
		i = web.input()
		#print i
		try:
			u = i['u']
		except:
			pass
		else:
			print u

def delete(id):
	if db.delete('images', where="id=$id", vars={'id' : id}):
		return "image id=%d deleted" % id
	else:
		return "no images with that id"

class logout:
	def GET(self):
		users.logout()

class show:
	def GET(self, page=1):
		#print delete(54)
		print 'Request from ip %s page %s' % (web.ctx.ip, page)
		######
		path = web.ctx.path
		print path.split('/')[1]
		if path and path.split('/')[1] == 'all':
			gallery = list(db.select('images', order="created DESC"))
		else:
			gallery = list(db.select('images', order="created DESC", where="public=$true", vars={'true' : 1}))
		total = len(gallery)
		pages = len(gallery) / ImagesOnPage
		page = int(page)
		if len(gallery) % ImagesOnPage:
			pages += 1
		return render.gallery(gallery[(page - 1) * ImagesOnPage:page * ImagesOnPage], pages, total, ret, page, path.split('/')[1])

#===================VARIABLES==========================================
urls = (
	'/', 'show',
	'/page/(\d+)', 'show',
	'/all', 'show',
	'/all/page/(\d+)', 'show',
	'/add', 'add',
	'/login', 'login',
	'/logout', 'logout',
	'/admin', admin.app,
	'/register', 'register',
	'/user/(.*)', 'show',
	'/test', 'test',
)

app = web.application(urls, globals())
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer = {'username': None, 'loggedin': False, 'user_id': -1, 'permission': 0})
	web.config._session = session
else:
	session = web.config._session

def session_hook():
	web.ctx.session = session
	web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))

render = web.template.render('templates/', globals={'session': session, 'getName': users.getName})
web.ctx.render = render
db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')

#=======================================================================

if __name__ == "__main__":
	app.run()
