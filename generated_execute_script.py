import subprocess

subprocess.run(
    [
        "powershell",
        "-Command",
        r"chcp 65001; Get-ChildItem -Path 'C:\Users\gmyun\OneDrive\바탕 화면\매크로 테스트1' -File | Where-Object { $_.Name -like '*.docx' } | Move-Item -Destination 'C:\Users\gmyun\OneDrive\바탕 화면\매크로 테스트2'",
    ],
    encoding="utf-8",
    errors="ignore",
    check=True,
)
subprocess.run(
    [
        "powershell",
        "-Command",
        r"chcp 65001; Get-ChildItem -Path 'C:\Users\gmyun\OneDrive\바탕 화면\매크로 테스트2' -File | Where-Object { $_.Name -like '*.docx' } | Compress-Archive -DestinationPath 'C:\Users\gmyun\OneDrive\바탕 화면\매크로 테스트2/archive.zip'",
    ],
    encoding="utf-8",
    errors="ignore",
    check=True,
)
