import logging
import tornado.web
import tornado.ioloop
import tornado.locks
import tornado.options

from tornado.options import define, options

define(name='debug', default=True, type=bool, help='调试模式')
define(name='port', default=8000, type=int, help='http 端口')


logging.basicConfig(level=logging.INFO)

class Application(tornado.web.Application):
    def __init__(self) -> None:
        handlers = [
            (r'/', 'handlers.HomeHandler'),
        ]
        settings = {
            'debug': options['debug'],
        }
        super().__init__(handlers, **settings)


async def main():
    tornado.options.parse_config_file('./config.py')
    app = Application()
    app.listen(options['port'])
    logging.info('Server is running at http://127.0.0.1:%s/' % options['port'])
    shutdown = tornado.locks.Event()
    await shutdown.wait()


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.run_sync(main)