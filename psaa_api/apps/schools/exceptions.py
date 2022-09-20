from rest_framework.exceptions import APIException


class SchoolNotFound(APIException):
    status_code = 404
    default_detail = 'School does not exist'

class IsiboNotFound(APIException):
    status_code = 404
    default_detail = 'Isibo does not exist'


class StudentDoesNotExist(APIException):
    status_code = 404
    default_detail = 'Student does not exist'
