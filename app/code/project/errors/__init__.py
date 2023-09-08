import sqlite3
from werkzeug.exceptions import HTTPException

ERRORS = {
    'OperationalError': sqlite3.OperationalError,
    'IntegrityError': sqlite3.IntegrityError
}


class MissingParameters(HTTPException):
    code = 400
    description = "Missing parameter"


class ResourceNotFound(HTTPException):
    code = 404
    description = "Resource not found in the database"


class NameResolutionError(HTTPException):
    code = 404
    description = "Resource not found in this URL."


class BadParameter(HTTPException):
    code = 400
    description = "Bad Parameter"


class OperationalError(HTTPException):
    code = 503
    description = "Database or Table not available"


class IntegrityError(HTTPException):
    code = 409
    description = "This resource already exist"
