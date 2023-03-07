import tornado.web
import pymongo.collection
import pymongo.database


class BaseHandler(tornado.web.RequestHandler):
    def get_collection(self, name: str) -> pymongo.collection.Collection:
        """ 获取数据表 """
        db: pymongo.database.Database = getattr(self.application, 'db')
        return db.get_collection(name=name)
