from enum import StrEnum


class FolderTargetDetail(StrEnum):
    FOLDER_NAME = "FOLDER_NAME"  # 폴더 이름만 작업
    FOLDER_PATH = "FOLDER_PATH"  # 폴더 경로 작업
    FOLDER_METADATA = "FOLDER_METADATA"  # 폴더 메타데이터 작업
    FOLDER = "FOLDER"  # 폴더 전체 작업 (이름, 경로 포함)
    FOLDER_SIZE = "FOLDER_SIZE"  # 폴더 크기 작업
    FOLDER_OWNER = "FOLDER_OWNER"  # 폴더 소유자 작업
    FOLDER_PERMISSIONS = "FOLDER_PERMISSIONS"  # 폴더 권한 작업
    FOLDER_CREATION_DATE = "FOLDER_CREATION_DATE"  # 폴더 생성 시간 작업
    FOLDER_MODIFICATION_DATE = "FOLDER_MODIFICATION_DATE"  # 폴더 수정 시간 작업
    FOLDER_ACCESS_DATE = "FOLDER_ACCESS_DATE"  # 폴더 접근 시간 작업
