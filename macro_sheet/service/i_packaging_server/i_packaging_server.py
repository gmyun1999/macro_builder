from abc import ABC, abstractmethod


class PackagingClientInterface(ABC):
    @abstractmethod
    def send_to_package_server(self, script_content: str) -> str:
        """
        패키징 서버에 스크립트를 업로드하고 GUI 다운로드 링크를 반환한다.
        """
        pass
