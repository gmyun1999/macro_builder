from enum import StrEnum


class FileConditionType(StrEnum):
    FILE_NAME_STARTSWITH = "file_name_startswith"  # 파일 이름 시작
    FILE_NAME_ENDSWITH = "file_name_endswith"  # 파일 이름 끝
    FILE_CONTAINS = "file_contains"  # 파일 포함
    FILE_EXTENSION = "file_extension"  # 파일 확장자
    FILE_SIZE_GT = "file_size_gt"  # 파일 사이즈 greater then
    FILE_CREATION_TIME_LT = "file_creation_time_lt"  # 파일 생성일 less then
    FILE_MODIFICATION_TIME_GT = "file_modification_time_gt"  # 파일 수정 시간 greater then
    FILE_OWNER = "file_owner"  # 파일 소유자
    FILE_PERMISSIONS = "file_permissions"  # 파일 권한
