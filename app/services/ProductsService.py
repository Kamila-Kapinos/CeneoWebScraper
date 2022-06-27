from app.services.DBService import DBService

class ProductsService(dict):

    __instance__ = None

    __db = None

    def __new__(cls, *args, **kwargs):
        if ProductsService.__instance__ is None:
            ProductsService.__instance__ = dict.__new__(cls)
            ProductsService.__instance__.__db = DBService().get_db()

        return ProductsService.__instance__

    def get_products(self):
        mycursor = self.__db.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM products')
        return mycursor.fetchall()

    def get_product(self, product_id):
        mycursor = self.__db.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM products WHERE products.id = %s', (str(product_id), ))
        return mycursor.fetchone()


    def add_product(self, product):
        mycursor = self.__db.cursor(dictionary=True)

        sql = "INSERT INTO `products` (`id`, `name`) VALUES (%s, %s)"
        val = (product.product_id, product.product_name)

        mycursor.execute(sql, val)
        self.__db.commit()
        return mycursor.lastrowid


    def update_product(self, product):
        mycursor = self.__db.cursor(dictionary=True)

        sql = "UPDATE products SET products.name = %s, products.average_score = %s, products.cons_count = %s, products.pros_count = %s, products.opinions_count = %s WHERE products.id = %s"
        val = (str(product.product_name), float(product.average_score), int(product.cons_count), int(product.pros_count), product.opinions_count, str(product.product_id))

        print(sql, val)

        mycursor.execute(sql, val)
        self.__db.commit()
