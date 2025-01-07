from macro_be import settings
from macro_sheet.infra.s3 import S3Storage
from macro_sheet.service.i_storage.i_storage import IStorage


class RecorderGuiService:
    def __init__(self) -> None:
        self.recorder_storage: IStorage = S3Storage(
            access_key_id=settings.RECORDER_S3_ACCESS_KEY,
            secret_access_key=settings.RECORDER_S3_SECRET_KEY,
            region_name="ap-northeast-2",
        )

    def get_recorder_gui_download_link(self) -> str | None:
        return self.recorder_storage.generate_presigned_url(
            bucket_name=settings.RECORDER_S3_BUCKET,
            object_key=settings.RECORDER_S3_OBJECT_KEY,
            expiration=300,
        )
