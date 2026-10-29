# 도구 준비와 인증

Skill 사용 지침과 설치 설정은 별개다. 핵심 TXT/CSV/JSON 추출, 검증, 미디어 구간 계획은 Python 3.10+ 표준 라이브러리만 사용한다. PowerShell 예:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-optional.txt
.venv/Scripts/python -m playwright install chromium
```

가상환경 Python으로 명령을 실행한다. 필요한 패키지만 선택 설치해도 된다. 위 파일은 허용 범위이며 완전한 lockfile은 아니다. 검증 환경의 실제 버전은 validation.md 참조. DOCX는 `python-docx`, PDF는 `pypdf`, XLSX는 `openpyxl`, 실제 브라우저는 `playwright`와 Chromium이 필요하다. Linux는 Playwright 공식 설치 안내에 따라 시스템 의존성도 설치한다.

## OCR

[Tesseract 공식 설치 안내](https://tesseract-ocr.github.io/tessdoc/Installation.html)에 따라 OS용 바이너리를 설치하고 PATH에 추가한다. 한국어/영어 traineddata를 준비한 뒤 `tesseract --version`, `tesseract --list-langs`로 확인한다. 필요 시 도구 설치 방식에 맞춰 `TESSDATA_PREFIX`를 설정한다. 스캔 PDF 렌더링은 Poppler의 `pdftoppm`을 사용한다. OCR 스크립트는 단일 이미지용이다. 이미지 타일링과 표 구조 복원은 Skill 절차로 처리한다.

## 음성·영상

[FFmpeg 공식 다운로드](https://ffmpeg.org/download.html)에서 OS에 맞는 배포 안내를 확인해 설치하고 PATH에 `ffmpeg`, `ffprobe`를 둔다. 전사는 설치된 도구를 사용한다. 선택 사항인 로컬 [Whisper](https://github.com/openai/whisper)는 `python -m pip install openai-whisper`로 설치하며 FFmpeg, 모델 가중치 다운로드, 충분한 메모리가 필요하다. 모델은 명령의 `--model`로 선택한다. 한국어 정확도와 GPU 호환성은 별도 확인 대상이다.

## 웹 접근·API

익명 브라우저 캡처는 인증 불필요. 로그인 사이트는 사용자가 허용한 세션/계정과 쿠키 동의 절차가 필요하다. 인증 상태, cookie 값, HAR/trace는 비밀을 포함할 수 있어 커밋하지 않는다.

이 저장소에는 외부 모델 API 클라이언트가 없고 유료 서비스가 필수가 아니다. `.env.example`의 AI_*는 향후 별도 어댑터용 예약 변수이며 현재 코드가 읽지 않는다. 제공자를 선택하면 현재 공식 API 문서를 확인해 키를 OS/비밀 저장소에 설정하고 모델명/URL을 설정으로 주입한다. 실제 호출 전에는 API 검증 완료라고 보고하지 않는다. RUN_BROWSER_TESTS만 현재 테스트가 읽으며 `.env`를 자동 로드하지 않는다.

Git 푸시는 Git Credential Manager의 GitHub HTTPS 인증과 해당 저장소 쓰기 권한이 필요하다. 키/토큰을 명령 인자나 저장소 파일에 넣지 않는다.

## 해커톤 확장 도구

추가된 Skill 8개는 저장소 `.agents/skills/`에 설치되어 있다. 핵심 사용 예는 `$hackathon-workflow`와 `$analyze-tables`다. Cofa에서는 docs/hackathon.md의 제한을 먼저 적용한다.

- PDF/문서/표: 선택 의존성에 pandas와 reportlab을 추가했다. 기존 python-docx/openpyxl/pypdf와 함께 필요에 따라 별도 가상환경에 설치한다. 이번 검증의 python-docx 1.2.0, reportlab 5.1.0은 전역 환경 변경 없이 `work/toolkit-deps`에 설치했다. 일반 실행 시 자동 로드되지 않으므로 실제 사용 환경에 설치가 필요하다. 이 임시 폴더에는 Pillow 13도 포함되어 기존 fastembed의 Pillow<13 조건과 충돌 경고가 있었으므로 공용 PYTHONPATH에 추가하지 않는다.
- Jupyter: `python .agents/skills/jupyter-notebook/scripts/new_notebook.py --kind experiment --title "Data audit" --out work/data-audit.ipynb`. 생성기는 표준 라이브러리만 필요하며 커널 실행에는 별도 Jupyter 환경이 필요하다.
- PaddleOCR 공식 두 Skill: 일반 연습에서만 `paddleocr>=3.7.0` CLI와 PADDLEOCR_ACCESS_TOKEN이 필요하다. PADDLEOCR_BASE_URL은 선택 설정이다. 이번에는 Skill 파일만 설치했고 CLI/API 호출은 미실행이다.
- Chandra: 일반 연습에서 라이선스·하드웨어 조건 확인 후 별도 가상환경에 `chandra-ocr[hf]`를 설치한다. 이번에는 Skill 지침만 추가했고 엔진/가중치는 설치하지 않았다.
- `.env.example`의 브라우저 테스트 기본값은 0이다. Cofa 외의 허용된 개발 환경에서만 명시적으로 1을 설정한다.
