from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class UserRoles:
    ADMIN_ROLES = [UserRole.ADMIN]
    USER_ROLES = [UserRole.USER]
