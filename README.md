# my_skill

AI 활용 경진대회와 실무 문제 해결을 위한 Codex Skills. 요구사항 → 자료 준비 → 도구별 추출 → 추론 → 검증으로 연결한다. 특정 유료 모델/API 없이 핵심 예제를 실행할 수 있다.

## Skill 목록

| Skill | 역할 |
|---|---|
| [interview-requirements](.agents/skills/interview-requirements/SKILL.md) | 목표·사용자·입출력·제약·예외·성공 기준, 사실/가정/질문 분리 |
| [prepare-evidence](.agents/skills/prepare-evidence/SKILL.md) | 자료 목록·해시·중복·누락, 출처 위치가 유지되는 추출 |
| [extract-ocr](.agents/skills/extract-ocr/SKILL.md) | 이미지/스캔 문자·표, 영역·겹침과 중요 필드 검토 |
| [analyze-media](.agents/skills/analyze-media/SKILL.md) | 전사·장면 추출, 원본 시간·화자 불확실성과 경계 확인 |
| [inspect-browser](.agents/skills/inspect-browser/SKILL.md) | 웹 탐색·조작·재현, 접속 조건과 화면 근거 |
| [verify-results](.agents/skills/verify-results/SKILL.md) | 원본 대조·계산·반례·누락·미검증 보고 |
| [coordinate-work](.agents/skills/coordinate-work/SKILL.md) | 단계 선택·독립 작업 병렬화·예산·재개·최종 검증 |

## 준비 사항

Python 3.10+로 핵심 예제를 실행한다. PDF/DOCX/XLSX/브라우저/OCR/전사는 선택 도구가 필요하다. **설치·인증은 [docs/setup.md](docs/setup.md)**, 실제 검증 범위는 [docs/validation.md](docs/validation.md), 공식 문서·공개 Skill·후기 구분은 [docs/sources.md](docs/sources.md) 참조. `.env.example`에는 필요한/예약 변수만 있고 키는 없다.

## 사용 예시

이 저장소에서 Codex를 열고 자연어 또는 명시 호출을 사용한다.

```text
$interview-requirements 인터뷰 기록에서 목표와 중요 질문을 먼저 정리하고 요구사항별 검증 기준을 만들어 줘.
$coordinate-work 첨부 자료로 요구사항을 해결해 줘. examples/run-config.json을 읽고 상태를 work/run-001에 남겨 줘. 마지막에 verify-results로 검증해 줘.
$extract-ocr scan.pdf의 표를 원문 위치와 함께 추출하고 숫자·이름의 불확실성을 표시해 줘.
$inspect-browser 승인된 테스트 사이트의 검색 동작을 재현하고 기대/실제 동작을 비교해 줘.
```

루트에서 실행하는 합성 주문 예제 (출력 폴더는 새 경로 사용):

```powershell
python .agents/skills/prepare-evidence/scripts/prepare.py examples/input work/example --expected examples/expected.json
python .agents/skills/verify-results/scripts/verify.py examples/checks.json --report work/example/verification.json
python .agents/skills/analyze-media/scripts/segments.py 601 --chunk 300 --overlap 5 --output work/media-plan.json
python -m unittest discover -s tests -v
$env:RUN_BROWSER_TESTS = '1'
python -m unittest discover -s tests -v
```

첫 두 명령의 정상 결과는 2개 자료 extracted와 pass다. 누락/손상은 보고서에 남으며 이미 있는 결과를 덮어쓰지 않는다. 예제 요구사항은 [examples/requirements.json](examples/requirements.json), 정형 검사 계약은 verify-results의 references에 있다. 검사 pass는 명시한 검사의 통과이며 전체 의미상 정답 보장은 아니다.

## 저장과 다른 프로젝트 설치

이 GitHub 저장소에 커밋/푸시하면 버전 관리된다. 다른 프로젝트에서 자동으로 사용 가능해지는 것은 아니다.

다른 프로젝트에 필요한 **Skill 폴더 전체**를 복사해 `<프로젝트>/.agents/skills/<skill-name>/`에 둔다. 예: 이 저장소의 `.agents/skills/prepare-evidence`를 대상의 `.agents/skills/prepare-evidence`로 복사한다. SKILL.md만 복사하면 scripts/references가 빠진다. 기존 동명 폴더는 비교 후 통합하고 덮어쓰지 않는다. 공통으로 쓰려면 `~/.agents/skills/`에 설치할 수도 있다([공식 규격](https://learn.chatgpt.com/docs/build-skills)). 변경이 보이지 않으면 Codex를 다시 연다.

복사한 Skill의 스크립트 경로는 해당 Skill 위치를 기준으로 잡는다. README의 실행 명령은 이 저장소 루트 기준이므로 다른 프로젝트에서는 실제 경로로 바꾼다. 루트 예제·선택 의존성·docs는 자동 복사되지 않는다. 설치 도구 안내가 필요하면 이 저장소의 setup 문서를 참고한다. 모든 Skill은 독립 사용 가능하며 전체 흐름은 7개를 함께 설치하는 편이 편리하다.

## 검증 상태와 한계

핵심 추출/정형 검사와 합성 자료의 누락·오류·경계 사례를 실행했다. 실제 Chromium 로컬 화면 캡처도 실행했다. OCR 엔진, 실제 전사/영상 디코딩, 로그인 사이트, 외부 모델 API, 대회 플랫폼 제출/채점은 검증 완료가 아니다. coordinate-work의 예산/체크포인트는 에이전트가 적용하는 절차이며 자동 스케줄러가 아니다. 자세한 실행 결과는 docs/validation.md에 기록한다.

원본/개인정보/인증 상태는 커밋하지 않는다. `work/`는 기본 제외된다. 새 작업 브랜치에서 검증 후 관련 변경만 푸시한다.
