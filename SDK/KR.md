# GRPE SDK

이 폴더에는 자연어 지시를 Gemini로 보내고, 생성된 셸 명령을 로컬 환경에서 실행하는 경량 Python SDK가 포함되어 있습니다.

## 파일 구성

- grpe_sdk.py
  - SDK의 메인 모듈입니다.
  - set_api(), ask_gemini(), grpe()를 제공합니다.
  - 현재 운영 체제와 명령 실행 기록을 포함한 프롬프트를 Gemini에 보내고, 생성된 명령을 셸로 실행합니다.

- color.py
  - 터미널 색상 출력을 위한 ANSI 이스케이프 코드를 정의합니다.
  - 주로 콘솔 스타일링 용도이며, 핵심 SDK 로직은 포함하지 않습니다.

## 필요 패키지

- Python 3.8 이상
- google-genai

다음 명령으로 설치할 수 있습니다.

```bash
pip install google-genai
```

## 기본 사용 방법

```python
import grpe_sdk

grpe_sdk.set_api("YOUR_GEMINI_API_KEY")

output = grpe_sdk.grpe("현재 디렉터리의 파일 목록을 보여줘")
print(output)
```

## 동작 방식

1. set_api()로 Gemini API 키를 저장합니다.
2. grpe() 함수가 현재 운영 체제와 이전 명령 기록을 포함한 프롬프트를 구성합니다.
3. Gemini가 명령 문자열을 반환합니다.
4. SDK가 subprocess를 사용해 해당 명령을 실행하고 표준 출력을 반환합니다.

## 참고 사항

- 생성된 명령은 셸을 통해 실행되므로, 스크립트가 실행되는 환경에 따라 결과가 달라질 수 있습니다.
- 모델이 올바른 명령을 생성하지 못하면 함수는 None을 반환하거나 오류 메시지를 출력합니다.
- 이 SDK는 간단한 명령 생성 및 실행 흐름용이며, 완전한 프로덕션급 자동화 도구로 설계된 것은 아닙니다.
