import web
from hashlib import md5

db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')

def addUser(name, password, permission='user'):
	n = db.insert('users', name=name, password=password, permission=permission)
	return 'ok'

def getName(id):
	check = db.select('users', where="id=$id", vars={'id' : id})
	if check:
		return check[0].name
	else:
		return 'No user with id=%d' % id
		
def login(i):
	session = web.ctx.session
	pswd = md5(i.password).hexdigest()
	check = db.select('users', where="name=$n AND password=$pswd", vars={'n' : i.username, 'pswd' : pswd})
	if check:
		user = check[0]
		session.loggedin = True
		session.username = user.name
		session.user_id = user.id
		session.perm = user.permission
		return web.seeother('/')
	else:
		return 'login error'

def logout():
	session = web.ctx.session
	session.kill()
	return web.seeother('/')
		
#class login:
	
	#def GET(self):
		#print web.ctx.session
		#return web.ctx. render.login()

	#def POST(self):
		#session = web.ctx.session
		#i = web.input()
		#pswd = md5(i.password).hexdigest()
		#check = db.select('users', where="name=$n AND password=$pswd", vars={'n' : i.username, 'pswd' : pswd})
		#if check:
			##print "Check.perm: %s" % check[0].password
			#user = check[0]
			#session.loggedin = True
			#session.username = user.name
			#session.user_id = user.id
			#session.perm = user.permission
			#return web.seeother('/')
		#else:
			#return 'error'

#class logout:
	#def GET(self):
		#session = web.ctx.session
		#session.kill()
		#return web.seeother('/')

if __name__ ==  '__main__':
	#print getName(2)
	pass
