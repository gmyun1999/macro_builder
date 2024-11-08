from abc import ABC, abstractmethod


class IPackageStorage(ABC):
    """
    s3같은곳에 패키징한 파일들을 저장한다.
    이 파일들에 대한 crud를 정의한다.
    서버가 추가되거나 바뀌면 repo 구현체 추가하거나 바꾸면됨.
    """

    @abstractmethod
    def delete_gui_package(self, gui_url: str):
        """
        gui_url을 가지는 gui package가 저장되어있는 저장소의 데이터를 삭제함
        """
        pass

    @abstractmethod
    def bulk_delete_gui_package(self, gui_urls: list[str]):
        """
        gui_url을 가지는 gui package가 저장되어있는 저장소의 데이터를 삭제함
        """
        pass
