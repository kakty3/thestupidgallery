import web
#from main import *

urls = (
	'', 'login',
)

class login:
	def GET(self):
		print session
		if not session.loggedin:
			return render.login()

	def POST(self):
		return 0


#===================VARIABLES==========================================
app = web.application(urls, globals())
#if web.config.get('_session') is None:
s = web.session.Session(app, web.session.DiskStore('admin_sessions'), {'username' : 0, 'loggedin' : 0})
	#web.config._session = s
#else:
	#s = web.config._session
render = web.template.render('templates/admin')  
#=======================================================================


