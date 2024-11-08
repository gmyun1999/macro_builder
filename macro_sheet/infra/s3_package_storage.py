from macro_sheet.service.i_package_storage.i_package_storage import IPackageStorage


class S3PackageStorage(IPackageStorage):
    """
    s3에 패키징한 파일들을 저장
    create 는 직접 다루지않고 packing 서버에서 다룰거임
    """

    def delete_gui_package(self, gui_url: str):
        """
        gui_url을 가지는 gui package가 저장되어있는 저장소의 데이터를 삭제함
        """
        pass

    def bulk_delete_gui_package(self, gui_urls: list[str]):
        """
        gui_url을 가지는 gui package가 저장되어있는 저장소의 데이터를 삭제함
        """
        pass
