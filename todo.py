__author__ = 'dn3'

class ToDo:
    def __init__(self, id, task, status, user):
        self.id = id
        self.task = task
        self.status = status
        self.user = user

    def render(self):
        todo = "{'id': '%s', 'task': '%s', 'status':'%s', 'user':'%s'}" % (self.id, self.task, self.status, self.user,)
        return todo.encode('ascii','ignore')


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def render(self):
        user = "{'id': '%s', 'username': '%s'}" % (self.id, self.username,)
        return user.encode('ascii','ignore')