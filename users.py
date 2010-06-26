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
		check = db.select('users', where="name=$n AND password=$pswd", vars={'n' : i.username, 'pswd' : pswd})
		if check:
			#print "Check.perm: %s" % check[0].password
			user = check[0]
			session.loggedin = True
			session.username = user.name
			session.user_id = user.id
			session.perm = user.permission
			return web.seeother('/')
		else:
			return 'error'

class logout:
	def GET(self):
		session.kill()
		return web.seeother('/')
