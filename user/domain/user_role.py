from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"


class UserRoles:
    ADMIN_ROLES = [UserRole.ADMIN]
    USER_ROLES = [UserRole.USER]
    ALL_USER_ROLES = [UserRole.USER, UserRole.GUEST]
