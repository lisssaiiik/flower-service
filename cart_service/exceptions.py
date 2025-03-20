from fastapi import HTTPException, status


class FlowersException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(FlowersException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(FlowersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(FlowersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(FlowersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(FlowersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(FlowersException):
    status_code = status.HTTP_401_UNAUTHORIZED


class IncorrectRoleException(FlowersException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Вы не являетесь админом"


class IncorrectFlowerIDException(FlowersException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Неверный ID цветка"
