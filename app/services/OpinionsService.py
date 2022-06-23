from datetime import datetime
from app.services.DBService import DBService

class OpinionsService(dict):

    __instance__ = None

    __db = None

    def __new__(cls, *args, **kwargs):
        if OpinionsService.__instance__ is None:
            OpinionsService.__instance__ = dict.__new__(cls)
            OpinionsService.__instance__.__db = DBService().get_db()

        return OpinionsService.__instance__

    def get_product_opinions(self, product_id):
        mycursor = self.__db.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM opinions WHERE opinions.product_id = %s', (str(product_id), ))
        return mycursor.fetchall()


    def add_product_opinion(self, product_id, opinion):
        mycursor = self.__db.cursor(dictionary=True)

        sql = "INSERT INTO `opinions` (`product_id`, `opinion_id`, `author`, `recommendation`, `stars`, `content`, `useful`, `useless`, `publish_date`, `purchase_date`, `pros`, `cons`)"
        sql += " VALUES (%s, %s,  %s,  %s,  %s,  %s, %s,  %s,  %s,  %s,  %s,  %s)"
        
        publish_date = datetime.strptime(opinion.publish_date, '%Y-%m-%d %H:%M:%S')
        # datetime.datetime(opinion.purchase_date)

        val = (str(product_id), str(opinion.opinion_id), str(opinion.author), str(opinion.recommendation), str(opinion.stars), str(opinion.content), 
            int(opinion.useful), int(opinion.useless), publish_date, publish_date, str(opinion.pros), str(opinion.cons))

        mycursor.execute(sql, val)
        self.__db.commit()
        return mycursor.lastrowid


    def clear_product_opinions(self, product_id):
        mycursor = self.__db.cursor(dictionary=True)

        sql = "DELETE FROM opinions WHERE opinions.product_id = %s"
        
        val = (str(product_id), )
        print(sql, val)

        mycursor.execute(sql, val)
        self.__db.commit()