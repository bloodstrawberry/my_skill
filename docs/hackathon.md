# 해커톤 적용 프로필

확인일 2026-10-29. 현재 작업은 대회 전 공개 도구 준비다. 사용 가능 여부는 사용자가 제공한 SK하이닉스·Cofa 안내로 판단하고, AI TOP 100은 문제 유형/해결 방식의 참고로 사용한다.

## Cofa 조건

- 필수 브리프 p1, 상세 가이드 p5: 제공 Codex 사용, Astra 제한, 외부 AI 모델/개인 API 키 금지, 문제·작업 파일·결과 외부 전송 및 Git Push 금지. 브리프 p1: Computer Use 전 단계 금지. Playwright 등 화면 자동 조작은 운영팀 확인 전 응시 경로에서 제외한다.
- 사용자 추가 공지: Codex 업데이트 금지. 권장 모델 6.1 Sol, 5.6 Terra, 6.0 Luna. 모델 선택은 제공 환경에서만 하며 설치/업데이트하지 않는다.
- 상세 p2~3: 실무자 에이전트에 업무 맥락 질문, Cofa Helper에 사용법 질문. 서버의 실제 포트와 0.0.0.0 바인딩 확인 후 플랫폼 Browser에서 사용자가 직접 확인한다.
- 브리프 p1, 상세 p3~5: 최대 작업 180분, 후속 서술형 6문항×5분, 14:00 전체 종료. 화면 예시의 5문항을 실제 규칙으로 쓰지 않는다. 후속 서술형 AI 사용 금지.
- Proctor 가이드 p1: 휴대폰 설치·연결·충전과 촬영 구도를 사전 점검한다. 감독 기능을 자동 조작하거나 변경하지 않는다.
- 공개 자료는 가져올 수 있지만 결과물을 통째로 대체하지 않는다. 개인 PC 파일 업로드는 금지. 이 저장소는 API로 공개 상태를 확인했으며 2차 예선 결과 통지 전까지 공개 유지가 필요하다. 지속 감시는 설정하지 않았다.

## 스킬 선택

| 작업 | Skill | Cofa 상태 |
|---|---|---|
| 전체 흐름 | hackathon-workflow / coordinate-work | 제공 도구로 적용 |
| 질문/근거/검증 | interview-requirements / prepare-evidence / verify-results | 로컬 처리 |
| 표 정제·조인·집계 | analyze-tables | pandas/openpyxl 로컬 |
| 문서·PDF·실험 | write-deliverables / pdf / jupyter-notebook | 로컬 처리 |
| 기본 OCR | extract-ocr (Tesseract) | OCR 엔진도 학습 모델을 사용하므로 별도 모델 금지와의 경계는 운영팀 확인 필요 |
| 문자 OCR | paddleocr-text-recognition | 공식 Skill은 외부 API 방식, 응시 중 호출 금지 |
| 표·수식·배치 | paddleocr-doc-parsing | 공식 Skill은 외부 API 방식, 응시 중 호출 금지 |
| 손글씨·복잡한 구조 | ocr-chandra | 별도 모델, 응시 중 사용 제외 |
| 웹 자동 조작 | inspect-browser | 응시 중 제외; 사용자 직접 미리보기 + 로컬 코드 테스트 |
| 음성·영상 | analyze-media | FFmpeg 변환과 별도 ASR 모델 구분, 외부 ASR 제외 |

설치된 Skill과 실행 엔진/가중치는 다르다. PaddleOCR API 토큰이나 Chandra 모델을 이 저장소에 저장하지 않는다. 공개 Skill 설치만으로 시험 사용 허가가 생기지 않는다.

## AI TOP 100에서 참고한 구성

[공식 소개](https://aitop100.org/about)는 OCR과 사진·영상·통화·문서·엑셀을 연결하는 업무 문제, 도구 배분과 결과 검증을 설명한다. [2026 공식 안내](https://aitop100.org/)는 인터뷰로 문제를 정의하고 제작한 에이전트를 평가하는 방식이다. 따라서 요구사항 인터뷰 → 자료별 처리 → 구현 → 실제 입출력 평가 → 결정/검증 기록을 채택했다. Cofa의 허용 도구 범위와는 별개다.

## 채택 기준과 라이선스

공개 사용 횟수 대신 저장소 별 5,000개 이상, 비보관 상태, 최근 유지보수, 명확한 기능/라이선스를 선정 기준으로 사용했다. 이 수치는 개별 Skill 설치 수가 아니다. 측정 원문은 toolkit-sources.json. 자체 통합 지침에는 사용량이 있다고 주장하지 않는다.

OpenAI skills 28,387 / PaddleOCR 91,933 / Tesseract 77,228 / Chandra 12,630 / pandas 50,338 / python-docx 5,752 stars (확인 시점).

공개 원본 설치: openai/skills commit 49f948faa9258a0c61caceaf225e179651397431의 pdf, jupyter-notebook. 각 LICENSE.txt 보존. Jupyter 경로만 프로젝트용 안내 추가.
PaddleOCR commit dab3fe35379033fdcb2d0e9572fac0b36c9a9ebf의 공식 두 Skill 설치, Apache-2.0 라이선스 보존 및 Cofa 실행 제한 추가.
Chandra는 공식 Skill을 복제한 것이 아니라 공식 CLI 기반 자체 지침. 코드 Apache-2.0과 모델 MODEL_LICENSE/상업적 자체 호스팅 조건은 별도로 검토해야 한다. 모델은 설치/배포하지 않았다.

문서·표의 과거 openai/skills doc/spreadsheet 경로는 현재 버전에 없어 설치하지 않았으며, 검증된 pandas/python-docx 도구용 자체 작업 지침으로 보완했다. 외부 배포·유료 API 생성·희소 서비스 연동 Skill은 이번 준비에서 제외했다.
