import web, main
from hashlib import md5
from main import *

urls = (
	'/', 'g',
	'/page/(.*)', 'g',
	'/add', 'add',
)

db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')

def addUser(name, password, permission='user'):
	n = db.insert('users', name=name, password=password, permission=permission)
	return 'ok'
	
class login:
	def GET(self):
		print main.session
		return render.login()

	def POST(self):
		i = web.input()
		pswd = md5(i.password).hexdigest()
		check = db.select('users', where="name=$n AND password=$pswd",vars={'n' : i.username, 'pswd' : pswd})
		if check: 
			session.loggedin = True
			session.username = i.username
			return web.seeother('/')
		else:
			return 'error'

class logout:
	def GET(self):
		session.kill()
		return web.seeother('/')
