from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    s3같은곳에 패키징한 파일들을 저장한다.
    이 파일들에 대한 crud를 정의한다.
    서버가 추가되거나 바뀌면 repo 구현체 추가하거나 바꾸면됨.
    """

    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        region_name: str | None = None,
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name

    @abstractmethod
    def delete_file(self, gui_url: str):
        pass

    @abstractmethod
    def bulk_delete_file(self, gui_urls: list[str]):
        pass

    def generate_presigned_url(
        self,
        bucket_name,
        object_key,
        expiration=300,
    ) -> str | None:
        """프리사인드 URL을 생성한다."""
        pass
