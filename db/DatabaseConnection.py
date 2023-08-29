import sqlite3

class DatabaseConnection:
    def __init__(self, db_name = 'medalsDB', init = True):
        self.db_name = db_name
        self.conn : sqlite3.connect = None
        if (init):
            self.connect()

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
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def execute(self, sql, args = None, ret = False):
        if (self.conn):
            self.cursor.execute(sql, args = args)
            if (ret): # if you need return something.
                if (ret == 'all'):   # return all.
                    return self.cursor.fetchall()
                elif (ret == 'one'): # return once.
                    return self.cursor.fetchone()
            else:
                return True
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def commit(self):
        if (self.conn is not None):
            self.conn.commit()
            return True
        else:
            raise sqlite3.OperationalError('没有连接数据库')

    def close(self):
        if self.conn:
            self.conn.close()