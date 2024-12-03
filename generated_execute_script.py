import subprocess

import requests


def send_recorder_data_6c3e83c05f91441f97729895e1d6236f():
    host = "127.0.0.1"
    port = 1000
    api_key = "test_key"
    endpoint = "/execute_recorder/"
    url = f"http://{host}:{port}{endpoint}"

    headers = {"Content-Type": "application/json", "Api-Key": api_key}
    recorder_data = {
        "mouse_events": [
            {"type": "mouse_move", "timestamp": 0.6201746463775635, "x": 728, "y": 345},
            {"type": "mouse_move", "timestamp": 0.62746262550354, "x": 735, "y": 356},
            {"type": "mouse_move", "timestamp": 0.6348810195922852, "x": 751, "y": 387},
            {"type": "mouse_move", "timestamp": 0.6421928405761719, "x": 778, "y": 431},
            {"type": "mouse_move", "timestamp": 0.6504206657409668, "x": 800, "y": 464},
        ],
        "keyboard_events": [
            {"type": "keyboard_press", "timestamp": 8.471685409545898, "key": "t"},
            {"type": "keyboard_press", "timestamp": 8.564444303512573, "key": "e"},
            {"type": "keyboard_press", "timestamp": 8.65369200706482, "key": "s"},
            {"type": "keyboard_press", "timestamp": 8.720302104949951, "key": "t"},
        ],
    }

    try:
        response = requests.post(url, json=recorder_data, headers=headers)
        if response.status_code == 200:
            print("recorder 실행 성공")
        else:
            print("recorder 실행 실패")
    except Exception as e:
        print(f"에러: {str(e)}")


def send_recorder_data_f1cb9e28a44c47d68f345674ff619201():
    host = "127.0.0.1"
    port = 1000
    api_key = "test_key"
    endpoint = "/execute_recorder/"
    url = f"http://{host}:{port}{endpoint}"

    headers = {"Content-Type": "application/json", "Api-Key": api_key}
    recorder_data = {
        "mouse_events": [
            {"type": "mouse_move", "timestamp": 0.6201746463775635, "x": 728, "y": 345},
            {"type": "mouse_move", "timestamp": 0.62746262550354, "x": 735, "y": 356},
            {"type": "mouse_move", "timestamp": 0.6348810195922852, "x": 751, "y": 387},
            {"type": "mouse_move", "timestamp": 0.6421928405761719, "x": 778, "y": 431},
            {"type": "mouse_move", "timestamp": 0.6504206657409668, "x": 800, "y": 464},
        ],
        "keyboard_events": [
            {"type": "keyboard_press", "timestamp": 8.471685409545898, "key": "t"},
            {"type": "keyboard_press", "timestamp": 8.564444303512573, "key": "e"},
            {"type": "keyboard_press", "timestamp": 8.65369200706482, "key": "s"},
            {"type": "keyboard_press", "timestamp": 8.720302104949951, "key": "t"},
        ],
    }

    try:
        response = requests.post(url, json=recorder_data, headers=headers)
        if response.status_code == 200:
            print("recorder 실행 성공")
        else:
            print("recorder 실행 실패")
    except Exception as e:
        print(f"에러: {str(e)}")


def send_recorder_data_62e92e6d784046ce9ec1d0bc44f68b7c():
    host = "127.0.0.1"
    port = 1000
    api_key = "test_key"
    endpoint = "/execute_recorder/"
    url = f"http://{host}:{port}{endpoint}"

    headers = {"Content-Type": "application/json", "Api-Key": api_key}
    recorder_data = {
        "mouse_events": [
            {"type": "mouse_move", "timestamp": 0.6201746463775635, "x": 728, "y": 345},
            {"type": "mouse_move", "timestamp": 0.62746262550354, "x": 735, "y": 356},
            {"type": "mouse_move", "timestamp": 0.6348810195922852, "x": 751, "y": 387},
            {"type": "mouse_move", "timestamp": 0.6421928405761719, "x": 778, "y": 431},
            {"type": "mouse_move", "timestamp": 0.6504206657409668, "x": 800, "y": 464},
        ],
        "keyboard_events": [
            {"type": "keyboard_press", "timestamp": 8.471685409545898, "key": "t"},
            {"type": "keyboard_press", "timestamp": 8.564444303512573, "key": "e"},
            {"type": "keyboard_press", "timestamp": 8.65369200706482, "key": "s"},
            {"type": "keyboard_press", "timestamp": 8.720302104949951, "key": "t"},
        ],
    }

    try:
        response = requests.post(url, json=recorder_data, headers=headers)
        if response.status_code == 200:
            print("recorder 실행 성공")
        else:
            print("recorder 실행 실패")
    except Exception as e:
        print(f"에러: {str(e)}")


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
for _ in range(3):
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
    for _ in range(3):
        send_recorder_data_6c3e83c05f91441f97729895e1d6236f()
    send_recorder_data_f1cb9e28a44c47d68f345674ff619201()
    send_recorder_data_62e92e6d784046ce9ec1d0bc44f68b7c()
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
