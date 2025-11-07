from fastapi import HTTPException, status

class FlowersException(HTTPException):
    status_code = 500
    detail = "Внутренняя ошибка сервера"

    def __init__(self, detail: str = None, status_code: int = None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectFlowerIDException(FlowersException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Неверный ID цветка"


class InvalidPriceException(FlowersException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Некорректная цена"


class InvalidQuantityException(FlowersException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Некорректное количество"


class EmptyFieldException(FlowersException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Поле не может быть пустым"
