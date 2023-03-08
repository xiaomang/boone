import string
import random
import pymongo.cursor
import bson
from typing import Any

def rand_str(length:int)->str:
    """ 生成随机字符串 """
    scope = string.ascii_letters+string.hexdigits
    res = ''
    for _ in range(length):
        res += random.choice(scope)
    return res

def res_format(obj:Any):
    """  """
    if isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            k = 'id' if k=='_id' else k
            res[k] = res_format(v)
        return res
    elif isinstance(obj, (tuple, list, pymongo.cursor.Cursor)):
        return [res_format(x) for x in obj]
    elif isinstance(obj, bson.ObjectId):
        return str(obj)
    else:
        return obj