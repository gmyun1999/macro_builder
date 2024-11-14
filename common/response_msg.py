from enum import StrEnum

MESSAGE = "message"


class TokenMessage(StrEnum):
    """
    .name -> code
    .value -> message
    """

    VALID = "This is a valid token."
    WRONG_TYPE = "It's wrong token type."
    EXPIRED = "Token is expired."
    NOT_FOUND = "Request header does not have token."
    ROLE_NO_PERMISSION = "Cannot access contents with your role!"


class LoginMessage(StrEnum):
    """
    .name -> code
    .value -> message
    """

    LOGIN_SUCCESS = "Login successfully"
    LOGIN_FAIL = "ID and password does not match our data."
    REQUIRED_PWD_CHANGE = "Please change your password!"
