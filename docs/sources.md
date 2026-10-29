# 출처와 채택 판단

확인일: **2026-10-29 (Asia/Seoul)**. 링크 원문을 직접 열어 확인했다. Skill/스크립트는 이 저장소 목적에 맞춰 직접 작성했으며 외부 Skill 파일을 복사하거나 번들하지 않았다. 원격 main과 stable 문서는 이후 바뀔 수 있다.

## 공식 규격·도구

| 출처 | 확인 내용 / 적용 |
|---|---|
| [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) ([기존 Codex URL](https://developers.openai.com/codex/skills/)) | name/description, 점진적 로드, 저장소 `.agents/skills` 검색, 수동 작성 및 명시 호출 |
| [OpenAI AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 저장소 작업 지침의 역할과 계층 |
| [pypdf 추출](https://pypdf.readthedocs.io/en/stable/user/extract-text.html) | 페이지별 텍스트와 OCR/배치 한계 |
| [python-docx](https://python-docx.readthedocs.io/en/latest/) | 문단/표 접근, 고정 페이지 대신 논리 위치 |
| [openpyxl](https://openpyxl.readthedocs.io/en/stable/) | 시트·셀 접근; 수식 재계산과 구분 |
| [Tesseract CLI](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) | 언어/PSM/TSV. confidence는 정답 인증으로 쓰지 않음 |
| [FFmpeg 공식 문서 소스](https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/doc/ffmpeg.texi) | 입력/출력, -ss/-t/-frames:v. ffmpeg.org HTML은 조회 시간 초과여서 공식 저장소 원문으로 확인 |
| [Whisper 공식 저장소](https://github.com/openai/whisper) | 로컬 CLI, 모델 선택, FFmpeg 의존. 설치/전사는 미실행 |
| [Playwright Python 설치](https://playwright.dev/python/docs/intro), [Page API](https://playwright.dev/python/docs/api/class-page) | Chromium, goto/locator/screenshot. 실제 로컬 페이지로 확인 |

## 공개 Skill 조사 (실제 파일·개별 라이선스 확인)

| 후보 | 기능·라이선스 | 판단 |
|---|---|---|
| [OpenAI playwright SKILL.md](https://github.com/openai/skills/blob/main/skills/.curated/playwright/SKILL.md), [원문](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/playwright/SKILL.md), [LICENSE.txt](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/playwright/LICENSE.txt) | npx/CLI로 탐색·스크린샷·UI 흐름 디버깅. 해당 디렉터리 Apache-2.0 | 재사용 가능한 선택지다. 이 저장소는 Python/연결 브라우저도 지원하고 접속 조건·재현 기록을 포함해야 해서 별도 Skill 작성 |
| [OpenAI pdf SKILL.md](https://github.com/openai/skills/blob/main/skills/.curated/pdf/SKILL.md), [원문](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/pdf/SKILL.md), [LICENSE.txt](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/pdf/LICENSE.txt) | Poppler 렌더링과 pypdf/pdfplumber 추출·시각 확인. 해당 디렉터리 Apache-2.0 | PDF 전용 작업에는 적합. 다형식 목록·중복/누락·출처 계약은 별도 구현 |

향후 실제로 복사/수정 배포하면 해당 버전의 라이선스·NOTICE 의무를 다시 확인하고 파일을 함께 보존한다. 이 문서의 조사만으로 다른 디렉터리까지 같은 라이선스라고 단정하지 않는다.

## 대회 공식 안내와 참가 경험의 구분

- [AI_TOP_100 공식 사이트](https://aitop100.org/): 2026 안내에서 가상 인물 인터뷰 후 AI 에이전트를 제작·제출하고 내부 평가 기준으로 심사한다고 확인했다. 이 저장소는 그 흐름에 맞춘 재사용 도구이며 공식 제출 규격/내부 채점 항목을 구현했다고 주장하지 않는다.
- [구혜승의 AI TOP 100 Campus 2026 본선 후기](https://kr.linkedin.com/posts/goohaeseung_3000%EB%AA%85-%EC%A4%91-100%EB%AA%85-ai-top-100-campus-2026-activity-7446949422493564928-tG6a): **비입상 참가자의 자기보고**다. Claude Code 조정, 소문항 병렬 처리, OCR/음성 도구 비교, 사람 개입 규칙, 쿠키 접속 조건과 검증 부족의 경험을 언급한다. Campus 회차 경험을 올해 하반기 대회 규칙이나 수상자 사용법으로 일반화하지 않는다. 모델별 속도/정확도 수치를 이 저장소에서 재현하지 않았으므로 추천 근거로 확정하지 않는다.
- **이 저장소의 제안**: 7개 역할, 요구사항 ID, SHA-256/위치 연결, Decimal 계산, 겹침 구간 계획, 설정 가능한 시도/동시 실행/시간 예산, JSON 체크포인트와 마지막 검증. 후기의 실제 구현이라고 서술하지 않는다.

## 해커톤 확장 조사 (2026-10-29)

이번 확장에는 공식 Skill 원본을 설치하고 LICENSE를 보존했다. 앞의 '외부 Skill을 복사하지 않았다'는 초기 7개 작성 시점 기록이다. 최신 설치 목록/고정 커밋/수정 범위는 [hackathon.md](hackathon.md)와 각 Skill의 UPSTREAM.md, 규모는 [toolkit-sources.json](toolkit-sources.json) 참조.

- https://aitop100.org/about 및 https://aitop100.org/ : 과거 다형식 문제와 올해 인터뷰·에이전트 방식.
- https://www.paddleocr.ai/main/en/version3.x/integrations/skills.html : 공식 두 Skill은 API 기반, 토큰 필요.
- https://github.com/datalab-to/chandra : 로컬 hf CLI와 코드/모델 라이선스 구분.
- 사용자 첨부 1_시험_필수확인사항_브리프.pdf p1, 2_Proctor_설치_및_촬영가이드.pdf p1, 3_사전_체험_및_응시환경_상세_가이드.pdf p1~5: Cofa 조건. 원본과 추출 전문은 공개 저장소에 포함하지 않았다.
