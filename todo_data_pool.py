__author__ = 'dn3'

from twisted.enterprise.adbapi import ConnectionPool, Transaction
from todo import ToDo
from todo import User


def _insertTodo(txn, task, user, status):
    txn.execute("INSERT INTO `todo` (task, user, status) VALUES (?, ?, ?)", (task, user, status))
    result = txn.fetchall()
    if result:
        return result
    else:
        return txn.lastrowid

def _updateTodo(txn, user, id, task, status):
    txn.execute("UPDATE `todo` SET task = ?,  status = ? WHERE id=? AND user=? ", (task, status, id, user,))
    txn.execute("SELECT * FROM `todo` WHERE id = ? and user =? ", (id, user,))
    result = txn.fetchall()
    if result:
        return result
    else:
        return txn.lastrowid

def _deleteTodo(txn, user, id):
    txn.execute("DELETE FROM `todo` WHERE user= ? AND id= ?", (user, id))
    return id

def build_todo(dbentries):
    id, task, status, user = dbentries[0]
    todo = ToDo(id, task, status, user)
    return todo

class DataPool:
    """
        Sqlite conn pool for ToDo
    """
    def __init__(self, dbname):
        self.dbname = dbname
        self.__dbpool = ConnectionPool('sqlite3', self.dbname)

    def shutdown(self):
        """
            Shutdown function: required task to shutdown the database connection pool:
        """
        self.__dbpool.close()

    def build_todos(self, dbentries):
        todos = []
        for dbentrie in dbentries:
            id, task, status, user = dbentrie
            todos.append( ToDo(id, task, status, user))
        return todos

    def build_todo(self, dbentries):
        id, task, status, user = dbentries[0]
        ToDo(id, task, status, user)
        return ToDo

    def get_todo_list(self, user):
        query = 'SELECT * FROM `todo` WHERE user=?'
        return self.__dbpool.runQuery(query, (user,)).addCallback(self. build_todos)

    def get_todo_by_id(self, user, id):
        query = 'SELECT * FROM `todo` WHERE user=? and id=?'
        return self.__dbpool.runQuery(query, (user, id,)).addCallback(self. build_todos)

    def create_todo(self, user, task):
        return self.__dbpool.runInteraction(_insertTodo, task, user, 0)

    def update_todo(self, user, id, task, status):
        return self.__dbpool.runInteraction(_updateTodo, user, id, task, status).addCallback(build_todo)

    def delete_todo(self, user, id):
        return self.__dbpool.runInteraction(_deleteTodo, user, id,)

    def return_login(self, dbentries):
        id, username, password = dbentries[0]
        user = User(id, username, password)
        return user

    def select_make_login(self, username, password):
        query = 'SELECT * FROM `users` WHERE username=? and password=?'
        return self.__dbpool.runQuery(query, (username, password,)).addCallback(self. return_login)