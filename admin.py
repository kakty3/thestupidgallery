import web
from hashlib import md5
#from main import *

urls = (
	'', 'login',
)

class login:
	def GET(self):
		print session
		if not session.loggedin:
			return render.login()
		else:
			return "WELCOME"

	def POST(self):
		i = web.input()
		pswd = md5(i.password).hexdigest()
		check = db.select('users', where="name=$n AND password=$pswd AND permission='admin'",vars={'n' : i.username, 'pswd' : pswd})
		if check: 
			session.loggedin = True
			session.username = i.username
			return "authorized"
		else:
			return 'error'


#===================VARIABLES==========================================
app = web.application(urls, globals())
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('admin_sessions'), initializer = {'username' : None, 'loggedin' : False})
	#web.config._session = session
else:
	session = web.config._session

def session_hook():
	web.ctx.admin_session = session
	web.template.Template.globals['session'] = session
	
render = web.template.render('templates/admin')
db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')
#=======================================================================


