# 블록기반 인터페이스 매크로빌더

## 시연영상
https://github.com/user-attachments/assets/e4079aa1-b47c-41c6-aa81-5ee1bebfa448


## Django 프로젝트 구동하기

이 README 파일은 기존 Django 프로젝트를 구동하는 방법을 안내합니다. 
이 프로젝트는 Dev Container를 사용하여 간단히 개발 환경을 설정할 수 있도록 구성되어 있습니다. Docker를 이용하려면 [docker](#7-docker)를 클릭하세요

## 목차
1. [Python 3.11 설치](#1-python-311-설치)
2. [Poetry 설치](#2-poetry-설치)
3. [프로젝트 의존성 설치](#3-프로젝트-의존성-설치)
4. [pre-commit 설정](#4-pre-commit-설정)
5. [mypy 설치 및 실행](#5-mypy-설치-및-실행)
6. [프로젝트 실행](#6-프로젝트-실행)
7. [docker](#7-docker)
## 1. Python 3.11 설치

1. 글로벌 하게 깔려면 [Python 공식 웹사이트](https://www.python.org/downloads/)에서 Python 3.11 버전을 다운로드합니다.
1-1. 저는 pyenv를 이용해서 까는걸 추천합니다.
2. 설치 과정에서 "Add Python 3.11 to PATH" 옵션을 선택하세요.
3. 설치 후, 터미널에서 다음 명령어로 버전을 확인합니다:
   ```
   python --version
   ```

## 2. Poetry 설치

1. 터미널에서 다음 명령어를 실행하여 Poetry를 설치합니다:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. 설치 후, Poetry가 정상적으로 설치되었는지 확인합니다:
   ```
   poetry --version
   ```

## 3. 프로젝트 의존성 설치

1. 프로젝트 디렉토리로 이동합니다:
   ```
   cd your-project-directory
   ```
2. Poetry를 사용하여 의존성을 설치합니다:
   ```
   poetry install
   ```

## 4. pre-commit 설정

1. pre-commit이 이미 `pyproject.toml`에 명시되어 있다면, 위의 `poetry install` 명령으로 설치되었을 것입니다.
2. pre-commit 훅을 설치합니다:
   ```
   poetry run pre-commit install
   ```
3. 모든 파일에 대해 pre-commit을 실행하려면:
   ```
   poetry run pre-commit run --all-files
   ```

## 5. mypy 설치 및 실행

1. mypy가 `pyproject.toml`에 명시되어 있지 않다면, 다음 명령어로 설치합니다:
   ```
   poetry add mypy
   ```
2. mypy를 실행하려면:
   ```
   poetry run mypy .
   ```

## 6. 프로젝트 실행

1. 가상환경 들어가기:
  ```
  poetry shell
  ```

2. Django 마이그레이션 실행:
   ```
   python manage.py migrate
   ```

3. Django 개발 서버를 실행합니다:
   ```
   python manage.py runserver
   ```
4. 웹 브라우저에서 `http://127.0.0.1:8000/`로 접속하여 프로젝트를 확인합니다.

## 7. docker

vscode 의 dev container와 vscode 를 사용하여 단 한번에 개발환경을 주인장과 동일하게 만듭니다.

1. [dev container vs extension 설치](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. VS Code Command Palette(Ctrl+Shift+P 또는 Cmd+Shift+P)를 열고, 다음 명령어를 실행합니다
   ```
   Remote-Containers: Reopen in Container
   ```
3. 기다립니다.
4. [프로젝트 실행](#6-프로젝트-실행)을 실행시킵니다.


