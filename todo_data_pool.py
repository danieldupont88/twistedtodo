__author__ = 'dn3'

from twisted.enterprise.adbapi import ConnectionPool, Transaction
from todo import ToDo


def _insertTodo(txn, task, user, status):
    txn.execute("INSERT INTO `todo` (task, user, status) VALUES (?, ?, ?)", (task, user, status))
    result = txn.fetchall()
    if result:
        return result[0][0]
    else:
        return txn.lastrowid

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

    def get_todo_list(self, user):
        query = 'SELECT * FROM `todo` WHERE user=?'
        return self.__dbpool.runQuery(query, (user,)).addCallback(self. build_todos)

    def get_todo_by_id(self, user, id):
        query = 'SELECT * FROM `todo` WHERE user=? and id=?'
        return self.__dbpool.runQuery(query, (user, id,)).addCallback(self. build_todos)

    def create_todo(self, user, task):
        return self.__dbpool.runInteraction(_insertTodo, task, user, 0)