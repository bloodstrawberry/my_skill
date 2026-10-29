# 요구사항 기록 예

```json
{
  "goal": {"value": "주문 합계 검증", "status": "confirmed", "evidence": ["interview.txt:line=12"]},
  "users": ["운영 담당자"],
  "inputs": ["CSV 주문"],
  "outputs": ["오류 주문 목록"],
  "constraints": [{"value": "외부 업로드 금지", "status": "confirmed", "evidence": ["brief.pdf:page=2"]}],
  "requirements": [{
    "id": "R-001", "statement": "합계 불일치를 보고한다", "status": "confirmed",
    "evidence": ["interview.txt:line=12"], "priority": "high",
    "acceptance": "1200+800=2000은 통과, 제출 합계 1900은 실패",
    "verification": "원본 셀 대조와 Decimal 재계산",
    "exceptions": ["금액 누락 시 미검증으로 보고"], "depends_on": []
  }],
  "questions": [{"id": "Q-001", "question": "통화가 다른 주문의 환산 기준은?", "impact": "합계 정의 변경", "blocks": ["R-002"]}]
}
```

이 예는 합성 자료다. 실전에서는 사용자, 입력, 출력, 예외, 성공 기준 각각에도 status와 evidence를 붙인다. 인터뷰 발언과 관찰된 동작을 구별한다. 검증 가능한 R-ID만 verify-results CASE로 옮기고 의미/사용성 평가는 manual로 남긴다.
