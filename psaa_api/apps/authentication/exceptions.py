from rest_framework.exceptions import APIException


class UserNotExist(APIException):
    status_code = 404
    default_detail = 'User does not exist'


class UserNotFound(APIException):
    status_code = 404
    default_detail = 'User not found'
    

class RoleNotFound(APIException):
    status_code = 404
    default_detail = 'Role does not exist'
