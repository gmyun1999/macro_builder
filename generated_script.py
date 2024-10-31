import subprocess


def func_nested_1():
    for _ in range(2):
        subprocess.run(
            [
                "powershell",
                "-Command",
                "Get-ChildItem -Path '/C/user/temp/' -File | Where-Object { $_.Length -gt 1000 } | Remove-Item",
            ]
        )
        subprocess.run(
            [
                "powershell",
                "-Command",
                "Get-ChildItem -Path '/C/user/images/' -File | Where-Object { $_.Extension -eq '.jpg' } | ForEach-Object { $_.FullName } | Out-File -FilePath '/C/user/image_list/file_list.txt' -Encoding UTF8",
            ]
        )


def func_nested_2():
    subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-ChildItem -Path '/C/user/logs/' -File | Where-Object { $_.Extension -eq '.log' } | Compress-Archive -DestinationPath '/C/user/compressed_logs/logs.zip'",
        ]
    )


if __name__ == "__main__":
    for _ in range(2):
        subprocess.run(
            [
                "powershell",
                "-Command",
                "Get-ChildItem -Path '/C/user/documents/' -File | Where-Object { $_.Extension -eq '.txt' } | Copy-Item -Destination '/C/user/backup'",
            ]
        )
        for _ in range(3):
            func_nested_1()
            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-ChildItem -Path '/C/user/downloads/' -File | Where-Object { $_.BaseName -like '*_old' } | Move-Item -Destination '/C/user/old_downloads/'",
                ]
            )
        for _ in range(3):
            func_nested_1()
            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-ChildItem -Path '/C/user/downloads/' -File | Where-Object { $_.BaseName -like '*_old' } | Move-Item -Destination '/C/user/old_downloads/'",
                ]
            )
        for _ in range(3):
            func_nested_2()
            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-ChildItem -Path '/C/user/downloads/' -File | Where-Object { $_.BaseName -like '*_old' } | Move-Item -Destination '/C/user/old_downloads/'",
                ]
            )
        func_nested_2()
