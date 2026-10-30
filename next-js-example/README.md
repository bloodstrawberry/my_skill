# Next.js UI starter

Ultra Office의 대시보드 구조(세로 메뉴, 헤더 검색, 도구 카드, 둥근 패널)를 참고해 새로 구현한 독립적인 UI 골격입니다. 원본의 업무 처리 코드나 유료 템플릿 파일을 복사하지 않았습니다.

## 실행

Node.js 20.9 이상, Yarn Classic 사용.

```sh
yarn install --frozen-lockfile
yarn dev
```

http://localhost:3000 에서 확인합니다. 서버는 0.0.0.0에 바인딩합니다.

```sh
yarn typecheck
yarn build
yarn start
```

## 포함 범위

- Next.js App Router + React + TypeScript
- MUI Material / Icons / Next.js SSR 캐시 + Emotion
- 반응형 사이드바, 접기/펼치기, 모바일 Drawer
- 전체 도구 카드와 카테고리 필터, 검색 모달(Ctrl/Cmd+K)
- 다크 모드와 메뉴 접기 상태의 로컬 저장
- 6개 작업 공간의 빈 화면과 존재하지 않는 경로의 404

파일 업로드·변환·OCR·AI·표/차트 엔진은 구현하지 않았으며 관련 라이브러리도 설치하지 않습니다. 대기 목록은 상위 `next_library.md`를 참고하세요. 폰트는 시스템 폰트를 사용하며 외부 CDN을 호출하지 않습니다.

## 확장 위치

- `src/components/office-shell.tsx`: 공통 레이아웃과 테마
- `src/lib/tools.ts`: 메뉴/카드 목록
- `src/app/page.tsx`: 홈 화면
- `src/components/tool-workspace.tsx`: 작업 공간 본문
- `src/app/tools/[slug]/page.tsx`: 도구 라우팅, 허용 slug 목록

새 도구를 추가하면 메뉴 목록과 라우트 slug 목록을 함께 갱신하세요. 필요한 기능 라이브러리는 과제가 확정된 뒤 개별적으로 설치하세요.

## 검증 기록 (2026-10-30)

| 요구사항 | 결과 | 근거 |
|---|---|---|
| Next.js UI 골격 | 통과 | TypeScript 검사와 production build 성공, 홈/6개 도구 페이지 HTTP 200 |
| 필요한 UI 패키지 설치 | 통과 | 실제 node_modules 확인, yarn.lock 생성 |
| 그 외 처리 라이브러리 대기 | 통과 | 직접 의존성 허용 목록 검사, PDF/OCR/Excel/FFmpeg/Mammoth/PptxGenJS 미설치 확인 |
| 라이브러리 문서 | 통과 | 상위 next_library.md에 우선순위·조건·출처 정리 |
| 메뉴/검색/필터/테마 | 확인 | 로컬 IAB에서 메뉴 열기·닫기, 작업 공간 이동, 검색 모달·빈 검색 결과, 문서 필터 2개, 다크/라이트 전환 확인 |
| 없는 도구 경로 | 통과 | /tools/missing HTTP 404 |

검증 환경: Node 24.22.1, Yarn 1.22.4, Next.js 16.4.3, React 19.3.1, MUI 7.3.11. 브라우저는 로그인 없는 로컬 IAB의 약 769px 폭에서 확인했다. 모든 화면 크기의 시각 회귀, 별도 데스크톱 viewport, Ctrl/Cmd+K 및 저장 상태의 재시작 복원은 별도 자동 테스트하지 않았다. 업무 처리/API 연결은 구현 범위 밖이다.

저장소 기존 검사 `python -m unittest discover -s tests -v`: 16개 통과, 브라우저 검사 1개 건너뜀. 이는 기존 스킬의 검사이며 새 UI의 브라우저 확인과 구분한다.
