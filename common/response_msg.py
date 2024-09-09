MESSAGE = "message"


class TokenMessage:
    VALID = "This is a valid token."
    WRONG_TYPE = "It's wrong token type."
    EXPIRED = "Token is expired."
    NOT_FOUND = "Request header does not have token."
    ROLE_NO_PERMISSION = "Cannot access contents with your role!"


class LoginMessage:
    LOGIN_SUCCESS = "Login successfully"
    LOGIN_FAIL = "ID and password does not match our data."
    REQUIRED_PWD_CHANGE = "Please change your password!"
