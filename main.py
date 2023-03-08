import logging
import tornado.web
import tornado.ioloop
import tornado.locks
import tornado.options
import pymongo
import pymongo.database

from tornado.options import define, options

define(name='debug', default=True, type=bool, help='调试模式')
define(name='port', default=8000, type=int, help='http 端口')
define(name='mongo_host', default='127.0.0.1', type=str, help='MongoDB IP')
define(name='mongo_port', default=27017, type=int, help='MongoDB端口')
define(name='mongo_database', default='mydata', type=str, help='MongoDB数据库名')
define(name='mongo_username', default='', type=str, help='MongoDB用户名')
define(name='mongo_password', default='', type=str, help='MongoDB密码')
define(name='mongo_auth_source', default='', type=str, help='MongoDB授权数据库')


logging.basicConfig(level=logging.INFO)


class Application(tornado.web.Application):
    def __init__(self, db: pymongo.database.Database) -> None:
        self.db = db
        handlers = [
            (r'/', 'handlers.HomeHandler'),
            (r'/users', 'handlers.UserHandler'),
            (r'/users/([a-f0-9]{24})', 'handlers.UserHandler'),
        ]
        settings = {
            'debug': options['debug'],
        }
        super().__init__(handlers, **settings)


async def main():
    tornado.options.parse_config_file('./config.py')

    conn = pymongo.MongoClient(
        host=options['mongo_host'],
        port=options['mongo_port'],
        username = options['mongo_username'],
        password =options['mongo_password'],
        authSource=options['mongo_auth_source'],
    )
    db = conn.get_database(options['mongo_database'])

    app = Application(db=db)
    app.listen(options['port'])
    logging.info('Server is running at http://127.0.0.1:%s/' % options['port'])
    shutdown = tornado.locks.Event()
    await shutdown.wait()


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.run_sync(main)
