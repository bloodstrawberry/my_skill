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
