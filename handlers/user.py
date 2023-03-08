import time

import bcrypt
import bson
import jsonschema
import tornado.escape
import tornado.ioloop

import utils
from exceptions import BadRequestError, NotFoundError
from handlers.base import BaseHandler


class UserHandler(BaseHandler):
    async def get(self, oid=None):
        projection = {'password': False}
        user_col = self.get_collection('users')
        if oid:
            filter = {'_id': bson.ObjectId(oid)}
            data = user_col.find_one(filter=filter, projection=projection)
            if not data:
                raise NotFoundError('用户不存在')
            res = utils.res_format(data)
        else:
            filter = {}
            sort = [('created', -1)]
            skip = self.get_skip_argument(0)
            limit = self.get_limit_argument(10)
            total = user_col.count_documents(filter)
            data = user_col.find(
                filter=filter,
                projection=projection,
                sort=sort,
                skip=skip,
                limit=limit,
            )
            res = {
                'total': total,
                'offset': skip,
                'limit': limit,
                'data': utils.res_format(data),
            }
        self.write(res)

    async def post(self):
        body = self.get_body()
        schema = {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {
                    'type': 'string',
                    'pattern': '^[a-z0-9]+@[a-z0-9-]+\.[a-z]+',
                },
                'password': {
                    'type': 'string',
                    'minLength': 8,
                    'maxLength': 32,
                }
            }
        }
        jsonschema.validate(body, schema)

        user_col = self.get_collection('users')
        if user_col.count_documents({'email': body['email']}):
            raise BadRequestError('邮箱已注册')

        ioloop = tornado.ioloop.IOLoop.current()
        hashed_password = await ioloop.run_in_executor(
            None,
            bcrypt.hashpw,
            tornado.escape.utf8(body['password']),
            bcrypt.gensalt(),
        )
        doc = {
            'email': body['email'],
            'nickname': 'uid-' + utils.rand_str(8),
            'password': hashed_password,
            'created': time.time(),
            'ip': self.request.remote_ip,
        }
        user_col.insert_one(doc)
        del doc['password']
        res = utils.res_format(doc)
        self.set_status(201)
        self.write(res)

    async def put(self, oid):
        filter = {'_id': bson.ObjectId(oid)}
        user_col = self.get_collection('users')
        doc = user_col.count_documents(filter)
        if not doc:
            raise NotFoundError('用户不存在')
        schema = {
            'type': 'object',
            'properties': {
                'nickname': {
                    'type': 'string',
                    'pattern': '^\w{2,10}$',
                }
            }
        }
        body = self.get_body()
        jsonschema.validate(body, schema)

        updated = {}
        nickname = body.get('nickname', None)
        if nickname:
            updated['nickname'] = nickname
        if updated:
            user_col.update_one(filter, {'$set': updated})
        entry = user_col.find_one(filter, {'password': False})
        res = utils.res_format(entry)
        self.write(res)

    async def delete(self, oid):
        filter = {'_id': bson.ObjectId(oid)}
        user_col = self.get_collection('users')
        doc = user_col.count_documents(filter)
        if not doc:
            raise NotFoundError('用户不存在')
        user_col.delete_one(filter)
