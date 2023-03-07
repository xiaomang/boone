class UnauthorizedError(Exception):
    """ 未登录 """

    status_code = 401


class ForbiddenError(Exception):
    """ 权限不够 """

    status_code = 403


class BadRequestError(Exception):
    """ 输入验证错误 """

    status_code = 400

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)


class ServerError(Exception):
    """ 服务器错误 """

    status_code = 500
