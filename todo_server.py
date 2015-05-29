__author__ = 'dn3'

import json
import cgi
from collections import namedtuple
from txrestapi.resource import APIResource
from txrestapi.methods import GET, POST, PUT, ALL, DELETE
from twisted.internet import reactor, defer
from twisted.web.server import Site, NOT_DONE_YET

from todo_data_pool import DataPool
from todo import ToDo


# We initialize the db pool with our dbname retrieved in the first step.
dbname='todo.db'
dbpool = DataPool(dbname)
ret_render = lambda todo: todo.render()

def get_todos(user):
    return dbpool.get_todo_list(user)

def get_todo(user, id):
    return dbpool.get_todo_by_id(user, id)

def make_login(username, password):
    return dbpool.select_make_login(username, password)

class ToDoAPI(APIResource):

    @GET('^/todos$')
    def get_list(self, request):
        print 'get todos'
        def onResult(data):
            request.setHeader(b"content-type", b"application/json")
            request.setHeader('Access-Control-Allow-Origin', '*')
            request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
            request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
            request.setHeader('Access-Control-Max-Age', 2520)
            response = json.dumps(data, default=lambda o: o.__dict__)
            request.write(response)
            request.finish()

        user = request.getHeader('user')
        print(user)

        data = get_todos(user)
        data.addCallback(onResult)
        return NOT_DONE_YET

    @GET('^/todos/(?P<id>[0-9]+)')
    def get_info(self, request, id):
        print 'get todo'
        def onResult(data):
            request.setHeader('Access-Control-Allow-Origin', '*')
            request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
            request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
            request.setHeader('Access-Control-Max-Age', 2520)
            request.setHeader(b"content-type", b"application/json")
            response = json.dumps(data, default=lambda o: o.__dict__)
            request.write(response)
            request.finish()

        user = request.getHeader('user')
        data = get_todo(user, id)
        data.addCallback(onResult)
        return NOT_DONE_YET

    @POST('^/todos$')
    def set_info(self, request):
        print 'post todo'

        def onResult(id):
            request.setHeader('Access-Control-Allow-Origin', '*')
            request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
            request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
            request.setHeader('Access-Control-Max-Age', 2520)
            todo = '{ "status": 0, "task": "'+ requestedTodo.task +'", "id": '+ str(id) + ', "user": "' + user + '" }'
            request.setHeader(b"content-type", b"application/json")
            request.write(todo.encode("utf-8"))
            request.finish()

        user = request.getHeader('user')
        payload = cgi.escape(request.content.read())
        requestedTodo = json.loads(payload, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        user = request.getHeader('user')

        dbpool.create_todo(user, requestedTodo.task).addCallback(onResult)
        return NOT_DONE_YET

    @PUT('^/todos/(?P<id>[0-9]+)')
    def create_ob(self, request, id):
        print 'put todo'
        def onResult(data):
            request.setHeader('Access-Control-Allow-Origin', '*')
            request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
            request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
            request.setHeader('Access-Control-Max-Age', 2520)
            request.setHeader(b"content-type", b"application/json")
            response = json.dumps(data, default=lambda o: o.__dict__)
            request.write(response)
            request.finish()

        user = request.getHeader('user')
        payload = cgi.escape(request.content.read())
        requestedTodo = json.loads(payload, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        request.setHeader(b"content-type", b"application/json")
        user = request.getHeader('user')

        d = dbpool.update_todo(user, id, requestedTodo.task, requestedTodo.status).addCallback(onResult)
        return NOT_DONE_YET

    @DELETE('^/todos/(?P<id>[0-9]+)')
    def del_ob(self, request, id):
        print 'delete todo'
        def onResult(data):
            request.setHeader('Access-Control-Allow-Origin', '*')
            request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
            request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
            request.setHeader('Access-Control-Max-Age', 2520)
            request.setHeader(b"content-type", b"application/json")
            request.write(data)
            request.finish()

        user = request.getHeader('user')
        d = dbpool.delete_todo(user, id).addCallback(onResult)
        return NOT_DONE_YET

    @POST('^/login/$')
    def user_login(self, request):
        print 'post login'
        def onResult(data):
            request.setHeader('Access-Control-Allow-Origin', '*')
            request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
            request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
            request.setHeader('Access-Control-Max-Age', 2520)
            request.setHeader(b"content-type", b"application/json")
            print data.id
            response = json.dumps(data, default=lambda o: o.__dict__)
            request.write(response)
            request.setHeader(b"logged-user", data.id)
            request.finish()

        def onError(err):
            request.setResponseCode(401)
            request.finish()

        payload = cgi.escape(request.content.read())
        requestedLogin = json.loads(payload, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        print requestedLogin.username
        print requestedLogin.password

        user = request.getHeader('user')
        data = make_login(requestedLogin.username, requestedLogin.password)
        data.addErrback(onError)
        data.addCallback(onResult)

        return NOT_DONE_YET

    @ALL('^/')
    def default(self, request):
        print "CORS HEADERS"
        request.setHeader(b"content-type", b"application/json")
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
        request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with,user,Content-Type')
        request.setHeader('Access-Control-Max-Age', 2520) # 42 hours
        #request.setResponseCode(404)
        request.finish()
        return NOT_DONE_YET

site = Site(ToDoAPI(), timeout=None)
reactor.listenTCP(8090, site)
reactor.run()