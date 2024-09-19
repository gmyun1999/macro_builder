from enum import StrEnum


class FolderConditionType(StrEnum):
    FOLDER_NAME_STARTSWITH = "folder_name_startswith"  # 폴더 이름 시작
    FOLDER_NAME_ENDSWITH = "folder_name_endswith"  # 폴더 이름 끝
    FOLDER_CONTAINS = "folder_contains"  # 특정 파일이나 하위 폴더 포함
    FOLDER_PATH = "folder_path"  # 특정 경로
    FOLDER_SIZE_GT = "folder_size_gt"  # 폴더 크기 greater than
    FOLDER_CREATION_TIME_LT = "folder_creation_time_lt"  # 폴더 생성일 less than
    FOLDER_MODIFICATION_TIME_GT = "folder_modification_time_gt"  # 폴더 수정 시간 greater than
    FOLDER_OWNER = "folder_owner"  # 폴더 소유자
    FOLDER_PERMISSIONS = "folder_permissions"  # 폴더 권한
    FOLDER_ITEM_COUNT_GT = "folder_item_count_gt"  # 폴더 내 아이템 수 greater than
    FOLDER_EMPTY = "folder_empty"  # 폴더가 비어있는지 여부
    FOLDER_DEPTH = "folder_depth"  # 폴더의 깊이 (예: 루트로부터의 수준)
