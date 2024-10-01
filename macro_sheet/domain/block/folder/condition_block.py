from enum import StrEnum


class FolderConditionType(StrEnum):
    FOLDER_NAME_STARTSWITH = "FOLDER_NAME_STARTSWITH"  # 폴더 이름 시작
    FOLDER_NAME_ENDSWITH = "FOLDER_NAME_ENDSWITH"  # 폴더 이름 끝
    FOLDER_CONTAINS = "FOLDER_CONTAINS"  # 특정 파일이나 하위 폴더 포함
    FOLDER_PATH = "FOLDER_PATH"  # 특정 경로
    FOLDER_SIZE_GT = "FOLDER_SIZE_GT"  # 폴더 크기 greater than
    FOLDER_CREATION_TIME_LT = "FOLDER_CREATION_TIME_LT"  # 폴더 생성일 less than
    FOLDER_MODIFICATION_TIME_GT = "FOLDER_MODIFICATION_TIME_GT"  # 폴더 수정 시간 greater than
    FOLDER_OWNER = "FOLDER_OWNER"  # 폴더 소유자
    FOLDER_PERMISSIONS = "FOLDER_PERMISSIONS"  # 폴더 권한
    FOLDER_ITEM_COUNT_GT = "FOLDER_ITEM_COUNT_GT"  # 폴더 내 아이템 수 greater than
    FOLDER_EMPTY = "FOLDER_EMPTY"  # 폴더가 비어있는지 여부
    FOLDER_DEPTH = "FOLDER_DEPTH"  # 폴더의 깊이 (예: 루트로부터의 수준)
