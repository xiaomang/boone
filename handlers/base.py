import tornado.web
import pymongo.collection
import pymongo.database
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):
    def get_skip_argument(self, default: int) -> int:
        """ 获取offset参数 """
        obj = self.get_argument('offset', default)
        return int(obj)
    
    def get_limit_argument(self, default: int) -> int:
        """ 获取limit参数 """
        obj = self.get_argument('limit', default)
        return int(obj)

    def get_body(self) -> dict:
        """ 获取body并将其转化成dict """
        body = self.request.body
        return tornado.escape.json_decode(body)

    def get_collection(self, name: str) -> pymongo.collection.Collection:
        """ 获取数据表实例 """
        db: pymongo.database.Database = getattr(self.application, 'db')
        return db.get_collection(name=name)
