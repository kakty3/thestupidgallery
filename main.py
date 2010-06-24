import web, os, admin
from urlparse import urlparse

ImagesOnPage = 10

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
			if not i:
				return render.add()
			try:
				name = i.n
				url = i.u
			except AttributeError:
				return 'Bad request'
			else:
				#return 'name=%s url=%s' % (name, url)
				if validUrl(url):
					n = db.insert('gallery', url=url, name=name)
					return 'name: %s\nurl: %s\nstatus: %s' % (name, url, 'posted')
				else:
					return 'url is not valid'
		else:
			return "Please, login to add pictures"

	def POST(self):
		i = web.input()
		#print i.url
		if validUrl(i.url):
			n = db.insert('gallery', url=i.url, name=i.name)
			raise web.seeother('/')
		else:
			return 'url is not valid'

class g:
	def GET(self, page=1):
		#print admin.app
		######
		gallery = list(db.select('gallery'))
		total = len(gallery)
		pages = len(gallery) / ImagesOnPage
		page = int(page)
		if len(gallery) % ImagesOnPage:
			pages += 1
		return render.gallery(gallery[(page - 1) * ImagesOnPage:page * ImagesOnPage], pages, total, ret, page)

#===================VARIABLES==========================================
urls = (
	'/', 'g',
	'/page/(\d+)', 'g',
	#'/addpic', 'addPicture',
	'/add', 'add',
	'/login', 'users.login',
	'/logout', 'users.logout',
	'/admin', admin.app,
	'/stat', 'statistic.show_sessions',
)

app = web.application(urls, globals())
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer = {'username' : None, 'loggedin' : False})
	web.config._session = session
else:
	session = web.config._session

def session_hook():
	web.ctx.session = session
	web.template.Template.globals['session'] = session
	
app.add_processor(web.loadhook(session_hook))

render = web.template.render('templates/', globals={'session': session})  
db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')
#=======================================================================

if __name__ == "__main__":
	app.run()
