# 실행 설정과 재개 계약

다음은 에이전트가 읽고 지키는 설정 예다. 백그라운드 실행기나 병렬 실행을 자동 구현하지 않는다. 도구별 실제 timeout과 동시 작업 수에 값을 적용하고 적용 여부를 기록한다.

```json
{
  "run_id": "example-001",
  "deadline_seconds": 900,
  "per_task_timeout_seconds": 120,
  "max_attempts_per_task": 2,
  "max_concurrency": 2,
  "max_no_progress_attempts": 2,
  "model_provider": null,
  "model_name": null,
  "network_allowed": false
}
```

- deadline은 최초 시작 UTC 시각+deadline_seconds다. 재개한다고 초기화하지 않는다.
- max_attempts는 최초 시도를 포함한다. 설정은 양의 정수, max_concurrency 기본 1도 가능하다. 실제 사용 가능한 슬롯 수를 넘기지 않는다.
- 한 작업의 timeout은 per_task_timeout과 남은 전체 시간 중 작은 값이다. timeout 후 자식 프로세스도 종료됐는지 확인한다.
- 독립성은 입력/출력뿐 아니라 브라우저 세션, GPU, 파일 lock, API 할당량도 포함한다.
- 진행은 새 검증 근거, 해결된 오류, 유효한 산출물의 증가다. 같은 오류/응답 반복은 무진전이다.

state 예:

```json
{
  "run_id": "example-001", "started_at": "2026-10-29T10:00:00Z",
  "deadline_at": "2026-10-29T10:15:00Z", "config_version": 1,
  "tasks": [{
    "id": "extract-01", "skill": "prepare-evidence", "depends_on": [],
    "status": "done", "attempts": 1, "no_progress_attempts": 0,
    "input_hashes": {"input/notes.txt": "actual-sha256"},
    "outputs": [{"path": "work/example/evidence.json", "sha256": "actual-sha256"}],
    "last_error": null
  }],
  "final_verification": {"status": "pending", "report": null}
}
```

위 hash는 설명용 값이며 실제 기록은 계산값으로 바꾼다. 상태는 pending/running/done/failed/blocked를 사용한다. 재개 때 running은 interrupted로 기록 후 예산을 확인하고 재실행 여부를 결정한다. done도 파일/해시가 맞지 않으면 pending으로 돌리고 하위 의존 작업도 무효화한다. 여러 작업은 별도 결과 파일에 쓰고 조정 담당만 state를 갱신한다.

올해 에이전트 제작 적용: 인터뷰 → 요구사항/질문 → 입력/출력·허용 도구 계약 → 자료 추출 → 해결 로직/실행 산출물 → 정상/예외 평가 → verify-results 보고. 이 순서는 저장소의 제안이며 공식 평가항목/제출 스키마는 제공되지 않은 한 추정하지 않는다.
