from abc import ABC, abstractmethod

from macro_be import settings


class IRecorderStorage(ABC):
    @abstractmethod
    def generate_presigned_url(
        self,
        bucket_name=settings.RECORDER_S3_BUCKET,
        object_key=settings.RECORDER_S3_OBJECT_KEY,
        expiration=300,
    ) -> str | None:
        """프리사인드 URL을 생성한다."""
        # S3 클라이언트 생성
        pass
