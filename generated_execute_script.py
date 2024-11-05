import subprocess

subprocess.run(
    [
        "powershell",
        "-Command",
        r"chcp 65001; Get-ChildItem -Path 'C:\Users\gmyun\OneDrive\바탕 화면\윤규민\test1' -File | Where-Object { $_.Extension -eq '.txt' } | Remove-Item",
    ],
    encoding="utf-8",
    errors="ignore",
    check=True,
)
