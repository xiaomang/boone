import time

from handlers.base import BaseHandler


class HomeHandler(BaseHandler):
    async def get(self):
        res = {
            'status': 'running',
            'time': time.time(),
        }
        self.write(res)
