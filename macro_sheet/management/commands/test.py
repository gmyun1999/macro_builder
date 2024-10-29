from django.core.management.base import BaseCommand

from macro_sheet.domain.block.file_system_block.file_system_block import (
    FileConditionDetail,
    FileSystemBlock,
)


class Command(BaseCommand):
    help = "Benchmark GenericSerializer deserialization performance"

    def handle(self, *args, **kwargs):
        # 테스트 데이터 정의 (20개의 경우)
        test_cases = [
            # 유효한 경우
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "COPY",
                "loc": "/C/user/homework/",
                "condition": [
                    {FileConditionDetail.FILE_EXTENSION: "pdf"},
                    {FileConditionDetail.FILE_SIZE_GT: "400"},
                ],
                "destination": "/C/user/Done",
                "rename": None,
            },  # 케이스 1: 유효한 복사
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "RENAME",
                "loc": "/C/user/homework/",
                "condition": [
                    {FileConditionDetail.FILE_EXTENSION: "pdf"},
                    {FileConditionDetail.NAME_ENDSWITH: "homework"},
                ],
                "destination": None,
                "rename": "숙제",
            },  # 케이스 2: 유효한 이름 변경
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "DELETE",
                "loc": "/C/user/homework/",
                "condition": [{FileConditionDetail.FILE_EXTENSION: "txt"}],
                "destination": None,
                "rename": None,
            },  # 케이스 3: 유효한 삭제
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FOLDER",
                "action": "MOVE",
                "loc": "/C/user/folder/",
                "condition": [{FileConditionDetail.FOLDER_SIZE_GT: "500"}],
                "destination": "/C/user/moved",
                "rename": None,
            },  # 케이스 4: 유효한 이동
            # 유효하지 않은 경우
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "COPY",
                "loc": "/C/user/homework/",
                "condition": [{FileConditionDetail.FILE_EXTENSION: "pdf"}],
                "destination": None,
                "rename": None,
            },  # 케이스 5: COPY에 destination 누락
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "RENAME",
                "loc": "/C/user/homework/",
                "condition": [{FileConditionDetail.FILE_EXTENSION: "pdf"}],
                "destination": None,
                "rename": None,
            },  # 케이스 6: RENAME에 rename 누락
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "COPY",
                "loc": "/C/user/homework/",
                "condition": [{FileConditionDetail.FILE_SIZE_GT: "0"}],
                "destination": "/C/user/Done",
                "rename": None,
            },  # 케이스 7: FILE_SIZE_GT 최소값 위반
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FOLDER",
                "action": "MOVE",
                "loc": "/C/user/folder/",
                "condition": [{FileConditionDetail.FILE_EXTENSION: "pdf"}],
                "destination": "/C/user/moved",
                "rename": None,
            },  # 케이스 8: FOLDER 대상에 파일 관련 조건
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "DELETE",
                "loc": "/C/user/folder/",
                "condition": [{FileConditionDetail.FOLDER_SIZE_GT: "500"}],
                "destination": None,
                "rename": None,
            },  # 케이스 9: FILE 대상에 폴더 관련 조건
            # 그 외 다양한 경우 추가
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "PRINT",
                "loc": "/C/user/reports/",
                "condition": [{FileConditionDetail.FILE_SIZE_LT: "1000"}],
                "destination": "/C/user/print_out",
                "rename": None,
            },  # 케이스 10: 유효한 출력
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FOLDER",
                "action": "COMPRESS",
                "loc": "/C/user/docs/",
                "condition": [{FileConditionDetail.FOLDER_SIZE_GT: "300"}],
                "destination": "/C/user/compressed",
                "rename": None,
            },  # 케이스 11: 유효한 압축
            # 유효하지 않은 더 많은 경우들
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "COMPRESS",
                "loc": "/C/user/images/",
                "condition": [{FileConditionDetail.FILE_EXTENSION: "jpg"}],
                "destination": None,
                "rename": None,
            },  # 케이스 12: COMPRESS에 destination 누락
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "MOVE",
                "loc": "/C/user/data/",
                "condition": [{FileConditionDetail.NAME_STARTSWITH: "2022"}],
                "destination": None,
                "rename": None,
            },  # 케이스 13: MOVE에 destination 누락
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "COPY",
                "loc": "/C/user/notes/",
                "condition": [],
                "destination": "/C/user/backup",
                "rename": None,
            },  # 케이스 14: 조건이 없는 유효한 복사
            # 추가 테스트 케이스들
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "RENAME",
                "loc": "/C/user/homework/",
                "condition": [{FileConditionDetail.NAME_STARTSWITH: "old_"}],
                "destination": None,
                "rename": "new_",
            },  # 케이스 15: 유효한 이름 변경
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FOLDER",
                "action": "PRINT",
                "loc": "/C/user/docs/",
                "condition": [
                    {FileConditionDetail.FOLDER_CREATION_TIME_GT: "2022-01-01"}
                ],
                "destination": "/C/user/logs",
                "rename": None,
            },  # 케이스 16: 유효한 폴더 출력
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "MOVE",
                "loc": "/C/user/images/",
                "condition": [{FileConditionDetail.FILE_SIZE_LT: "100"}],
                "destination": "/C/user/moved_small",
                "rename": None,
            },  # 케이스 17: 유효한 파일 이동
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FILE",
                "action": "COPY",
                "loc": "/C/user/data/",
                "condition": [{FileConditionDetail.FILE_EXTENSION: "csv"}],
                "destination": "/C/user/backups",
                "rename": None,
            },  # 케이스 18: 유효한 파일 복사
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FOLDER",
                "action": "COMPRESS",
                "loc": "/C/user/archives/",
                "condition": [{FileConditionDetail.FOLDER_SIZE_LT: "10000"}],
                "destination": "/C/user/compressed",
                "rename": None,
            },  # 케이스 19: 유효한 폴더 압축
            {
                "block_type": "FILE_SYSTEM_BLOCK",
                "target": "FOLDER",
                "action": "DELETE",
                "loc": "/C/user/temp/",
                "condition": [],
                "destination": None,
                "rename": None,
            },  # 케이스 20: 조건 없는 유효한 폴더 삭제
        ]

        # 테스트 실행
        for i, test_data in enumerate(test_cases, start=1):
            self.stdout.write(f"\n--- Test Case {i} ---")
            try:
                # DTO를 객체로 변환
                filesystem_block = FileSystemBlock.from_dto(test_data)

                # 검증 수행
                is_valid = filesystem_block.validate()
                self.stdout.write(
                    self.style.SUCCESS(f"Validation passed for case {i}.")
                )

                # PowerShell 코드 생성 테스트
                powershell_code = filesystem_block.to_powershell()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Generated PowerShell command:\n{powershell_code}"
                    )
                )

            except ValueError as e:
                self.stdout.write(
                    self.style.ERROR(f"Validation failed for case {i}: {e}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in case {i}: {e}"))
