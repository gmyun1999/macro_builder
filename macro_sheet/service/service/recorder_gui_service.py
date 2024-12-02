from macro_sheet.infra.s3_recorder_storage import S3RecorderStorage
from macro_sheet.service.i_recorder_storage.i_recorder_storage import IRecorderStorage


class RecorderGuiService:
    def __init__(self) -> None:
        self.recorder_storage: IRecorderStorage = S3RecorderStorage()

    def get_presigned_url(self) -> str | None:
        return self.recorder_storage.generate_presigned_url()
