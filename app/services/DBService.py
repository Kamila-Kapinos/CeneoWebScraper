import mysql.connector

from app.config.Config import Config

class DBService(dict):

    __instance__ = None

    __db = None

    def __new__(cls, *args, **kwargs):
        if DBService.__instance__ is None:
            DBService.__instance__ = dict.__new__(cls)
            mydb = mysql.connector.connect(
                host=Config['db']['host'],
                user=Config['db']['user'],
                password=Config['db']['password'],
                database=Config['db']['database']
            )
            DBService.__instance__.__db = mydb

        return DBService.__instance__

    def get_db(self):
        return self.__db