import web
from hashlib import md5

db = web.database(dbn='mysql', user='webpy', pw='webpy', db='gallery')

def addUser(name, password):
	if not db.select('users', where="name=$name", vars={'name' : name}):
		password = md5(password).hexdigest()
		n = db.insert('users', name=name, password=password, permission='user')
	else:
		return 1

def getName(id):
	check = db.select('users', where="id=$id", vars={'id' : id})
	if check:
		return check[0].name
	else:
		return 'No user with id=%d' % id
		
def login(i):
	print "trying to login"
	session = web.ctx.session
	pswd = md5(i.password).hexdigest()
	check = db.select('users', where="name=$n AND password=$pswd", vars={'n' : i.username, 'pswd' : pswd})
	if check:
		user = check[0]
		session.loggedin = True
		session.username = user.name
		session.user_id = user.id
		session.permission = user.permission
		return web.seeother('/')
	else:
		return 1

def logout():
	session = web.ctx.session
	session.kill()
	return web.seeother('/')

if __name__ ==  '__main__':
	#print getName(2)
	pass
