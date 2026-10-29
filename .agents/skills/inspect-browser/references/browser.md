# 재현 기록 형식

```text
requirement_id: R-UI-01
url / final_url:
captured_at: ISO 8601 with offset
browser/version / viewport / locale / timezone:
login: anonymous | authorized session (식별자는 비식별화)
cookie_consent: not shown | accepted | rejected | unknown
network: local | normal | restricted; observed HTTP status
steps: 시작 상태 → 관찰한 버튼 → 입력 → 대기 조건
expected:
actual:
artifacts: screenshot + DOM/text + 필요한 콘솔 오류(비밀 제거)
reproducibility: 횟수/성공률, 미확인 조건
```

Playwright 설치는 docs/setup.md 참조. 작업별 실제 조작은 `page.get_by_role(...).click()`와 관찰한 label 등을 쓴다. 로그인된 storage_state와 trace/HAR에는 비밀이 포함될 수 있어 저장소에 넣지 않는다. 제출/게시 권한은 읽기 접근 권한과 별개다.

capture.py는 timezone=UTC, locale=en-US, viewport=1280x720으로 새 context를 만든다. `--wait-selector`는 관찰한 선택자에만 사용한다. content와 screenshot은 동적 변화 때문에 완벽히 같은 시각이 아닐 수 있다. networkidle은 지속 연결 웹앱에서 완료 기준으로 쓰지 않는다. 캡처가 성공해도 버그 재현이나 로그인 기능 검증이 자동 완료되는 것은 아니다.
