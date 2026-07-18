# GRPE v2 Shell

이 폴더에는 설치 스크립트와 셸 명령 진입점을 포함한 GRPE 셸의 두 번째 버전이 들어 있습니다.

## 기능

- 인터랙티브 셸 사용
- 명령 실행기를 등록하는 설치 스크립트 제공
- 사용자의 홈 디렉터리에 API 키 저장
- 프롬프트 앞에 (talkmod)를 붙이면 대화형 출력 모드 사용 가능

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
2. 설치 스크립트를 실행합니다.

```bash
python install.py
```

3. 설정 프롬프트를 따라가며 명령 실행기 등록과 Gemini API 키 저장을 완료합니다.
4. macOS에서는 필요한 경우 셸 설정을 다시 불러옵니다.

```bash
source ~/.zshrc
```

5. 터미널에서 다음 명령으로 실행합니다.

```bash
grep e
```

프롬프트 앞에 (talkmod)를 붙이면 대화형 스타일의 응답을 사용할 수 있습니다.
