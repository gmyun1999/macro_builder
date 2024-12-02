import boto3

from macro_be import settings
from macro_sheet.service.exception.exceptions import (
    PresignedUrlGenerationException,
    S3ClientInitializationException,
)
from macro_sheet.service.i_recorder_storage.i_recorder_storage import IRecorderStorage


class S3RecorderStorage(IRecorderStorage):
    def generate_presigned_url(
        self,
        bucket_name=settings.RECORDER_S3_BUCKET,
        object_key=settings.RECORDER_S3_OBJECT_KEY,
        expiration=300,
    ) -> str | None:
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.RECORDER_S3_ACCESS_KEY,
                aws_secret_access_key=settings.RECORDER_S3_SECRET_KEY,
                region_name="ap-northeast-2",
            )

        except boto3.exceptions.NoCredentialsError as e:
            raise S3ClientInitializationException(
                message="AWS 자격 증명이 누락되었습니다.", detail={"error": str(e)}
            )
        except boto3.exceptions.Boto3Error as e:
            raise S3ClientInitializationException(
                message="S3 클라이언트 초기화 중 오류가 발생했습니다.", detail={"error": str(e)}
            )

        try:
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=expiration,  # 5분 (300초)
            )
            return presigned_url

        except boto3.exceptions.Boto3Error as e:
            raise PresignedUrlGenerationException(
                message="프리사인드 URL 생성 중 오류가 발생했습니다.", detail={"error": str(e)}
            )
