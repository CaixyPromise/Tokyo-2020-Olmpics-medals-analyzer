import sqlite3

class DatabaseConnection:
    db_name = 'medalsDB'
    def __init__(self, db_name = 'medalsDB', init = True):
        self.db_name = db_name
        self.conn : sqlite3.connect = None
        if (init):
            self.conn = self.connect()
        else:
            print('没有连接数据库, 调用connect()方法以连接数据库')

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    @property
    def cursor(self):
        if (self.conn is not None):
            return self.conn.cursor()
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def init_table(self, sql):
        if (self.conn):
            cur = self.cursor
            cur.execute(sql)
            self.commit(cur)
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def execute_manny(self, sql, data):
        if (self.conn):
            cur = self.cursor
            cur.executemany(sql, data)
            self.commit(cur)
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def execute(self, sql, args = None, ret = False, commit = False):
        if (self.conn):
            cur = self.cursor
            if (args):
                cur.execute(sql, args)
            else:
                cur.execute(sql)
            if (commit):
                self.commit(cur)
                return True
            if (ret): # if you need return something.
                if (ret == 'all'):   # return all.
                    return cur.fetchall()
                elif (ret == 'one'): # return once.
                    return cur.fetchone()
            else:
                return True
        else:
            raise sqlite3.OperationalError('没有连接数据库')
    def fetchall(self, cur):
        return cur.fetchall()

    def fetchone(self, cur):
        return cur.fetchone()

    def fetchmany(self, cur, size = 1):
        return cur.fetchmany(size)

    def commit(self, cur):
        if (self.conn is not None):
            self.conn.commit()
            return True
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def close(self):
        if self.conn:
            self.conn.close()
        else:
            raise sqlite3.OperationalError('没有连接数据库')