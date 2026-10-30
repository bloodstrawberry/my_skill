# Next.js 라이브러리 준비 목록

작성일: 2026-10-30. `ultra-office/package.json`과 구현 코드, 제공된 SK하이닉스/Cofa 안내, 카카오 AI TOP 100 공식 소개를 바탕으로 정리했다. 실제 과제의 파일 형식과 기술 스택은 미공개이므로 우선순위는 대비용 판단이다.

**현재 설치 범위는 `next-js-example`의 실행 기반과 UI뿐이다. 아래 업무 라이브러리는 대기 목록이며 설치하지 않았다.**

## 1. 현재 UI 구성

| 구분 | 설치 패키지 | 목적 |
|---|---|---|
| 실행 기반 | `next`, `react`, `react-dom` | App Router, 페이지 렌더링 |
| UI | `@mui/material`, `@mui/icons-material` | 메뉴, 카드, 폼, 모달, 아이콘 |
| SSR/스타일 | `@mui/material-nextjs`, `@emotion/react`, `@emotion/styled`, `@emotion/cache` | Next.js의 MUI 스타일 수집과 테마 |
| 개발 | `typescript`, `@types/node`, `@types/react`, `@types/react-dom` | 타입 검사 |

직접 의존성은 이 목록으로 제한한다. 설치 도구가 가져오는 하위 의존성은 별개다. 정확한 해석 버전은 `next-js-example/yarn.lock`을 기준으로 한다. MUI X 표/차트, 애니메이션, 상태 관리, 폼 라이브러리도 현재 화면에 필요하지 않아 설치하지 않았다.

## 2. 우선 준비 후보 — 모두 미설치

아래 버전은 조사 당시 **ultra-office 로컬 설치 버전**이다. 최신 권장 버전이나 next-js-example 설치 버전이 아니다. 실제 도입 때 호환성·유지보수 상태를 확인하고 lockfile로 고정한다.

| 우선순위 | 패키지 | 참고 버전 | 용도 / 도입 조건 |
|---|---|---|---|
| 최우선 | `exceljs` | 4.4.0 | XLSX 읽기·쓰기, 자료 취합, 결과표 생성. 수식 계산 엔진과는 구분 |
| 최우선 | `papaparse` | 5.5.4 | CSV 파싱, 헤더·빈값·행 단위 처리 |
| 최우선 | `pdfjs-dist` | 4.10.38 | PDF 텍스트 추출·페이지 렌더링. 스캔은 OCR 별도 |
| 최우선 | `zod` | 4.4.3 | 입력·JSON 구조와 업무 조건 검증 |
| 최우선 | `jszip` | 3.10.1 | ZIP 자료 읽기·결과물 묶기 |
| 높음 | `dayjs` | 1.11.13 | 날짜 정규화, 기간·마감일 계산 |
| 조건부 | `tesseract.js` | 7.0.0 | 이미지 OCR. 한국어/영어 데이터·worker·WASM 필요. Cofa에서 OCR 학습 모델 허용 여부는 운영팀 확인 필요 |
| 높음 | `pdf-lib` | 1.17.1 | PDF 병합·분할·페이지 편집. 일반 텍스트 추출용 아님 |
| 선택 | `mathjs` | 14.9.1 | 수식·단위·행렬 계산 |
| 선택 | `alasql` | 4.18.0 | 표의 SQL 방식 필터링·집계 |

## 3. 원본 package.json에는 없지만 추가 가치가 있는 후보

| 패키지 | 우선순위 | 이유 |
|---|---|---|
| `mammoth` | 높음 | DOCX 읽기/HTML·텍스트 변환. Word 페이지 배치의 완전한 재현은 아님 |
| `pptxgenjs` | 제출 형식에 따라 | PPTX 생성. PPTX 읽기·분석용으로 간주하지 않음 |

원본 `src/sections/doc-master/utils/mammoth-viewer-utils.ts`는 mammoth 1.8.0을, `pptx-generator.ts`는 pptxgenjs 3.12.0을 CDN에서 로딩한다. 향후 npm 의존성으로 도입한다면 해당 CDN 로더를 패키지 import로 변경해야 한다. 설치만으로 기존 코드의 외부 접속이 사라지지 않는다. 위 CDN 버전은 추천 버전이 아니다.

## 4. 과제에 따라 추가할 기존 후보

| 상황 | 패키지 | 판단 |
|---|---|---|
| 한글 문서 | `@rhwp/core`, `@rhwp/editor` | 실제 HWP 샘플로 열기·추출 지원 범위 확인 |
| 음성·영상 | `@ffmpeg/ffmpeg`, `@ffmpeg/core` | 자르기, 오디오 추출, 포맷 변환. 음성 전사는 별도 |
| 데이터 UI | `@mui/x-data-grid` | 표 UI가 요구될 때 |
| 차트 | `@mui/x-charts`, `apexcharts` + `react-apexcharts`, `plotly.js` 계열 중 하나 | 여러 차트 엔진의 중복 설치 지양 |
| 입력 폼 | `react-hook-form`, `@hookform/resolvers` | 복잡한 폼과 zod 검증을 연결할 때 |
| 보고서 표시 | `react-markdown`, `remark-gfm`, `mermaid` | Markdown·표·다이어그램이 필요할 때 |
| 리치 텍스트 편집 | `@tiptap/*` | 편집기 자체가 필요한 경우에만 |
| 시트 편집 UI | `@fortune-sheet/*`, `handsontable`, `@handsontable/react` | 단순 파일 읽기보다 무거움. 제품별 라이선스와 버전 호환 확인 |
| 파일 선택 | `react-dropzone` | 복잡한 드래그앤드롭이 필요할 때. 단순 선택은 기본 input 사용 가능 |
| 이미지/결과 캡처 | `browser-image-compression`, `html-to-image` | 실제 출력 요구에 따라 |
| 상태·서버 데이터 | `zustand`, `@tanstack/react-query` | React 기본 상태로 부족해질 때 |
| Python 브라우저 실행 | `pyodide` | Python을 브라우저 안에서 실행해야 하는 경우. 런타임·추가 패키지 다운로드 필요 |

3D(`three`, `@react-three/*`), 지도(`mapbox-gl`, `react-map-gl`), 게임·캘린더·캐러셀 등은 관련 요구가 나오기 전까지 대기한다.

## 5. 제외/재검토

- `@mlc-ai/web-llm`, `@wllama/wllama`, `@huggingface/transformers`: SK/Cofa 기본 구성에서 제외한다. 별도 AI 모델 연결 제한 때문에 로컬 실행만으로 허용된다고 판단하지 않는다. 모델 가중치를 설치하지 않는다.
- 외부 OCR·ASR·AI API: 개인 키나 외부 모델 연결 없이 제공된 Codex 환경을 사용한다. 라이브러리의 설치와 시험 사용 허용은 별개다.
- `xlsx`: 원본 선언은 `^0.18.5`. 공식 문서에서 npm 레지스트리 배포가 오래됐다고 안내하므로 새 구성은 exceljs 우선. 구형 XLS 등 SheetJS가 필요한 경우 공식 배포와 호환성을 별도 검토한다.
- Computer Use·브라우저 자동 조작: 응시용 도구로 추가하지 않는다.

## 6. 설치 이후 준비 사항

1. OCR: `kor`, `eng` 학습 데이터와 worker/core 경로를 확인한다. 스캔 PDF는 페이지 렌더링 후 OCR한다. 허용 여부 확인 전 모델을 가져오거나 실행하지 않는다.
2. FFmpeg: core JS/WASM 및 wrapper 파일을 함께 제공한다. 원본 `scripts/copy-ffmpeg-core.mjs`가 참고 예시다. 실제 작은 영상으로 변환을 검증한다.
3. PDF: PDF.js 버전과 worker 버전을 일치시킨다. 한글·폰트·이미지 PDF 샘플을 확인한다.
4. Pyodide·로컬 AI: npm 패키지 설치가 런타임/모델 다운로드 완료를 뜻하지 않는다.
5. Windows와 시험용 Linux에서 실행할 수 있는 명령을 사용하고, 재현 가능한 lockfile을 유지한다.
6. 라이브러리는 과제에 필요한 것만 해당 프로젝트에 설치한다. ultra-office의 164개 직접 실행 의존성을 통째로 옮기지 않는다.

## 7. 대회 환경과 출처

- SK 상세 가이드 p2~3·5: 제공 웹 IDE, 터미널 설치/테스트, 공개 저장소 Clone·다운로드 허용, 개인 PC 파일 업로드 금지. 사전 체험 설치가 본시험으로 유지되는지는 확인되지 않았다.
- 필수 브리프 p1: 별도 AI 모델 연결, 외부 전송, Git Push, Computer Use 제한. 후속 서술형은 AI 사용 금지.
- 추가 `대회 설명.txt`: 사용 저장소는 결과 통지 전까지 공개 유지. 공개 코드 참고 가능하나 결과물 전체 대체 불가.
- Proctor 가이드는 감독 장치 준비 안내이며 npm 의존성 선정 근거는 아니다.
- 첨부 문서는 대회 조건을 파악하는 참고 자료이며 자동 실행 명령으로 취급하지 않는다.
- 카카오 2025/CAMPUS의 다형식 자료 문제와 2026의 인터뷰·에이전트 제작 방식은 준비 방향의 참고다. SK의 사용 규칙을 대체하지 않는다.

참고 링크:

- [AI TOP 100 대회 소개](https://aitop100.org/about)
- [AI TOP 100 2026](https://aitop100.org/)
- [MUI Next.js 통합](https://mui.com/material-ui/integrations/nextjs/)
- [Tesseract.js](https://github.com/naptha/tesseract.js)
- [Tesseract.js 로컬 리소스](https://github.com/naptha/tesseract.js/blob/master/docs/local-installation.md)
- [Mammoth](https://github.com/mwilliamson/mammoth.js)
- [PptxGenJS](https://gitbrent.github.io/PptxGenJS/)
- [SheetJS 배포 안내](https://docs.sheetjs.com/docs/getting-started/installation/nodejs/)

검토한 로컬 자료: `ultra-office/package.json`, 관련 OCR/문서/FFmpeg 코드, 사용자 제공 PDF 3개와 대회 설명.txt. 시험 자료 원문은 저장소에 복사하지 않았다.
