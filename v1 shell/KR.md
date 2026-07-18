# GRPE v1 Shell

이 폴더에는 GRPE 셸 경험의 첫 번째 버전이 포함되어 있습니다.

## 기능

- 인터랙티브 프롬프트 기반 명령 실행
- Gemini 기반 명령 생성
- api.grpe 파일에 API 키 저장

## 필요 조건

- Python 3.8 이상
- pyfiglet
- google-genai

다음 명령으로 의존성을 설치할 수 있습니다.

```bash
pip install pyfiglet google-genai
```

## 사용 방법

1. 터미널에서 이 폴더를 엽니다.
2. 다음 명령으로 실행합니다.

```bash
python main.py
```

3. 프롬프트가 나오면 Gemini API 키를 입력합니다.
4. 자연어 명령을 입력하기 시작합니다.

## 자신의 프로젝트에서 SDK 사용하기

자신의 프로젝트에서도 CLI 도우미 모듈을 사용할 수 있습니다.

1. v1 shell/grpe_cli.py 파일을 프로젝트 폴더로 복사합니다.
2. grpe_cli를 가져옵니다.
3. cli() 함수를 사용해 텍스트 프롬프트로 명령을 생성하고 실행합니다.
