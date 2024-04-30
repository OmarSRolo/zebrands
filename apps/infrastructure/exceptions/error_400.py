from rest_framework.exceptions import APIException


class BaseError400(APIException):
    status_code: int = 400
    default_detail: str = 'Item not found, try again later.'
    default_code: str = 'Item_Not_Found'
