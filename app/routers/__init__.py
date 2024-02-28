from . import data, auth, test
routers = data.routers + [test.router] + [auth.router]