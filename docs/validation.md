# 검증 기록

실행일: **2026-10-29 (Asia/Seoul)**. Windows / Python 3.13.3. 기존 저장소는 README.md와 .gitattributes만 있었고 AGENTS.md, 언어/빌드 설정, 사용자 미커밋 변경은 없었다. 원격은 bloodstrawberry/my_skill. Git 소유자 차이는 전역 설정 대신 명령별 safe.directory로 한정 처리했다.

## 실제 실행

1. 다른 Skill 구현에 앞서 prepare-evidence와 verify-results를 작성했다. examples/input의 두 합성 파일에서 위치·SHA-256을 기록하고 1200+800=2000 및 인용을 검사하여 pass를 받았다. 초기 정상/오류 테스트 9개 통과 후 나머지를 작성했다.
2. 최종 `RUN_BROWSER_TESTS=1` 설정 후 `python -m unittest discover -s tests -v`: **17개 통과, 실패 0, 건너뜀 0**.
3. Skill Creator의 `quick_validate.py`를 각 폴더에 `python -X utf8`로 실행: **7개 모두 valid**. Windows cp949 기본 인코딩에서는 읽기 오류가 있었고 UTF-8 모드로 해결했다. 외부 검증기 파일은 수정하지 않았다.
4. `python -m compileall -q .agents/skills tests` 통과.
5. 미디어 구간 계획 CLI에 601초/300초/5초 겹침을 입력: [0,300), [295,595), [590,601) 생성. 실제 디코딩/전사는 수행하지 않았다.
6. 실제 Chromium 151.0.7922.34로 로컬 합성 HTML의 지연 로딩 조건을 기다린 뒤 Calculate를 클릭: Waiting → 2000 KRW 확인. 1900 KRW와 다름도 검사했다. 별도 capture.py로 익명 화면 PNG·본문·접속 조건을 수집하고 PNG를 열어 확인했다. 외부 사이트나 로그인 검증은 아니다.
7. OCR CLI 실행은 Tesseract 부재를 명확히 보고하고 결과를 생성하지 않았다. TSV 파서만 합성 엔진 출력으로 검사했다.
8. 예제의 파일 해시와 실제 산출물을 연결한 work/example/state.json을 작성했다. 이는 실행 후 작성한 재개 형식 예이며 자동 예산 집행/스케줄링의 실증이 아니다.

실제 패키지: pypdf 6.16.1, openpyxl 3.1.5, playwright 1.62.0, PyYAML 6.0.3. 이 버전 조합으로 검증했으며 Python 3.10 등 다른 버전/OS는 실행하지 않았다.

## 정상·오류·경계 사례

| 검사 | 관측 결과 |
|---|---|
| UTF-8 텍스트·여러 줄 CSV와 논리 행 위치 | 추출 및 위치 유지 |
| 중복 원본·예상 파일 누락·깨진 JSON | 중복/누락/파일별 error 분리 |
| 지원하지 않는 이미지·빈 텍스트 | needs_extraction/review_required로 남김 |
| 실제 텍스트 PDF / 빈 PDF | page=1 추출 / 빈 페이지 OCR 검토 경고 |
| 실제 XLSX 수식·숨김 시트 | 수식 원문/셀 위치 보존, 재계산하지 않음 |
| 0.1+0.2 / 잘못된 합계 / Infinity | Decimal 정상 / fail / 유한 숫자 검증 fail |
| 원본 변조·근거 누락·출처 경로 이탈 | fail |
| 요구사항 중복 ID | 잘못된 케이스로 거부 |
| 빈 검사·알 수 없는 검사·manual | unverified |
| 정형 검증 CLI 종료 코드 | pass=0, fail=1, unverified=2 |
| 원본/상하위 출력 폴더·기존 출력 덮어쓰기 | 거부 |
| 미디어 짧은 길이·정확한 경계·겹침·0/NaN/무한대 | 범위 커버 / 잘못된 입력 거부 |
| OCR 숫자/기호·낮은 점수·따옴표 토큰 | 합성 TSV 파싱/검토 후보 표시, 인식 품질은 미검증 |

## 미검증과 필요한 설정

- Tesseract 엔진/kor+eng 언어 데이터, Poppler가 필요하다. 실제 OCR, 이미지 타일링, 표 구조 복원과 숫자·이름 인식 품질은 미검증이다.
- FFmpeg/ffprobe와 로컬 ASR(또는 허용된 전사 서비스)이 필요하다. 실제 음성/영상, chunk 경계 전사, 화자·장면 정확도는 미검증이다.
- python-docx가 현재 없어 DOCX 경로는 미실행이다. 설치 후 머리글·텍스트박스 등 별도 시각 확인이 필요하다.
- 실제 웹 로그인/쿠키 동의·외부 사이트 조건, 외부 모델 API, 대회 플랫폼 제출/내부 채점은 수행하지 않았다. 코어/API 키 필수 의존성은 없다.
- 인터뷰, OCR 영역 분할, 사람 검토, 예산/재개 운영은 Skill 절차다. 자율 에이전트의 행동 평가나 장시간 중단/재개 스트레스 테스트 완료로 표시하지 않는다.

인증·설치는 [setup.md](setup.md), 참고 근거는 [sources.md](sources.md) 참조. 로컬 실행 산출물은 work/에 있고 Git에서 제외된다. 재실행 시 새 출력 폴더/보고서 경로를 사용한다.

## 해커톤 확장 검증 (2026-10-29)

- 전체 Skill 15개의 quick_validate.py 검사 통과(UTF-8 모드). 공식 다운로드 4개는 원본 라이선스·고정 커밋·로컬 변경 표시 보존.
- 기존 unittest 17개 중 16개 통과, 브라우저 1개는 명시적 선택 테스트로 건너뜀. 처음에는 읽기 전용 샌드박스의 임시 디렉터리 생성 제한으로 실패했으며 쓰기 가능한 권한으로 재실행하여 통과했다. 이번 변경에서 화면 자동 조작을 추가 실행하지 않았다.
- Jupyter 공식 생성기를 실행해 합성 노트북 생성 및 nbformat/cells 확인. 노트북 전체 커널 실행은 하지 않았다.
- pandas 합성 표 조인: ID 001 보존, 1200+800=2000, 키 중복 시 MergeError 확인.
- python-docx 합성 문서 저장 후 다시 열어 텍스트 일치 확인. DOCX 페이지 배치 렌더링은 미검증.
- ReportLab 합성 PDF 생성, pypdf 텍스트 확인, pypdfium2 렌더링 및 이미지 열람 확인.
- 첨부 PDF는 텍스트로 근거 위치를 확인하고 필수 브리프를 렌더링해 제한 사항을 대조했다. 원본 PDF·전문·로컬 패키지는 Git 제외.
- PaddleOCR API, Chandra 추론, 실제 OCR/음성 품질은 미검증. Skill 설치와 실행 엔진 설치를 구분한다.
- 문서·패키지 검증 중 자동 승인 검토의 사용량 한도로 한 명령이 미실행되었으나 사용자 재개 요청 후 동일 검증을 완료했다. Codex 버전 업데이트는 수행하지 않았다.
