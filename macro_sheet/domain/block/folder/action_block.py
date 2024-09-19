from enum import StrEnum


class FolderTargetDetail(StrEnum):
    FOLDER_NAME = "folder_name"  # 폴더 이름만 작업
    FOLDER_PATH = "folder_path"  # 폴더 경로 작업
    FOLDER_METADATA = "folder_metadata"  # 폴더 메타데이터 작업
    FOLDER = "folder"  # 폴더 전체 작업 (이름, 경로 포함)
    FOLDER_SIZE = "folder_size"  # 폴더 크기 작업
    FOLDER_OWNER = "folder_owner"  # 폴더 소유자 작업
    FOLDER_PERMISSIONS = "folder_permissions"  # 폴더 권한 작업
    FOLDER_CREATION_DATE = "folder_creation_date"  # 폴더 생성 시간 작업
    FOLDER_MODIFICATION_DATE = "folder_modification_date"  # 폴더 수정 시간 작업
    FOLDER_ACCESS_DATE = "folder_access_date"  # 폴더 접근 시간 작업
