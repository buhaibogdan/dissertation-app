import sqlite3
import datetime


class LogDB(object):
    def __init__(self):
        self.conn = sqlite3.connect("/home/bb/PycharmProjects/dissertation-app/db/log.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY,
                                    details text, date text, type INTEGER)
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_type (id INTEGER PRIMARY KEY,
                                    name text)
        """)

        self.__populateTypes()

    def __populateTypes(self):
        content = self.cursor.execute("SELECT exists(SELECT 1 FROM log_type LIMIT 1)").fetchone()
        if content is None:
            self.cursor.execute("""
                INSERT INTO log_type (id, name) VALUES (1, 'error')
            """)
            self.cursor.execute("""
                INSERT INTO log_type (id, name) VALUES (2, 'warning')
            """)
            self.cursor.execute("""
                INSERT INTO log_type (id, name) VALUES (3, 'notice')
            """)

    def getErrors(self):
        return self.__getLog(1)

    def getWarnings(self):
        return self.__getLog(2)

    def getNotices(self):
        return self.__getLog(3)

    def __getLog(self, type):
        return self.cursor.execute("""SELECT id, details, date FROM log WHERE type=?""", (type, )).fetchall()

    def insertError(self, message):
        a = self.__insertLog(message, 1)
        return a

    def insertWarning(self, message):
        self.__insertLog(message, 2)

    def insertNotice(self, message):
        self.__insertLog(message, 3)

    def __insertLog(self, message, type):
        sql = "INSERT INTO log (details, date, type) VALUES (?, ?, ?)"
        a = self.conn.execute(sql, (message, str(datetime.datetime.now()), type, ))

        self.conn.commit()
        return a

    def clear(self):
        self.conn.execute("DELETE FROM log")
        self.conn.commit()

logDB = LogDB()