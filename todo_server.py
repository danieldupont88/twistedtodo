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

class ToDoAPI(APIResource):

    @GET('^/todos/$')
    def get_list(self, request):

        def onResult(data):
            request.setHeader(b"content-type", b"application/json")
            response = json.dumps(data, default=lambda o: o.__dict__)
            request.write(response)
            request.finish()

        user = request.getHeader('user')

        data = get_todos(user)
        data.addCallback(onResult)
        return NOT_DONE_YET

    @GET('^/todos/(?P<id>[0-9]+)')
    def get_info(self, request, id):
        def onResult(data):
            request.setHeader(b"content-type", b"application/json")
            response = json.dumps(data, default=lambda o: o.__dict__)
            request.write(response)
            request.finish()

        user = request.getHeader('user')
        data = get_todo(user, id)
        data.addCallback(onResult)
        return NOT_DONE_YET

    @POST('^/todos/$')
    def set_info(self, request):

        def onResult(id):
            todo = '{ "status": 0, "task": "'+ requestedTodo.task +'", "id": '+ str(id) + ', "user": "' + user + '" }'
            request.setHeader(b"content-type", b"application/json")
            request.write(todo.encode("utf-8"))
            request.finish()

        user = request.getHeader('user')
        payload = cgi.escape(request.content.read())

        # Parse JSON into an object with attributes corresponding to keys.
        requestedTodo = json.loads(payload, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        user = request.getHeader('user')

        dbpool.create_todo(user, requestedTodo.task).addCallback(onResult)
        return NOT_DONE_YET

    @PUT('^/todos/(?P<id>[a-zA-Z0-9]+)')
    def create_ob(self, request, id):
        return "Trying to create object with id %s" % id

    @DELETE('^/todos/(?P<id>[a-zA-Z0-9]+)')
    def del_ob(self, request, id):
        return "Deleting object %s" % id

    @ALL('^/')
    def default(self, request):
        return "I match everything; clearly, you aren't asking for anything interesting."

site = Site(ToDoAPI(), timeout=None)
reactor.listenTCP(8090, site)
reactor.run()