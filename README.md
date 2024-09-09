# Django 프로젝트 구동하기

이 README 파일은 기존 Django 프로젝트를 구동하는 방법을 안내합니다. Poetry를 사용한 의존성 관리, pre-commit 설정, mypy 설치, 그리고 Python 3.11 사용에 대해 설명합니다.

## 목차
1. [Python 3.11 설치](#1-python-311-설치)
2. [Poetry 설치](#2-poetry-설치)
3. [프로젝트 의존성 설치](#3-프로젝트-의존성-설치)
4. [pre-commit 설정](#4-pre-commit-설정)
5. [mypy 설치 및 실행](#5-mypy-설치-및-실행)
6. [프로젝트 실행](#6-프로젝트-실행)

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

## 추가 명령어



