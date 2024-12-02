from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"


class UserRoles:
    ADMIN_ROLES = [UserRole.ADMIN.value]
    USER_ROLES = [UserRole.USER.value]
    ALL_USER_ROLES = [UserRole.USER.value, UserRole.GUEST.value]
