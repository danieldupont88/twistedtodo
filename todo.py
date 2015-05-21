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