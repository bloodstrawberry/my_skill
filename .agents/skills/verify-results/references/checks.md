# 정형 검사 계약

CASE JSON 경로를 기준으로 source_root와 evidence를 해석한다. 모든 requirements에 고유 id와 checks 배열을 둔다. 각 검사는 다음 중 하나다.

- source_quote: evidence_id, quote. 파일 SHA-256과 위치 유무, 추출 텍스트 내 인용을 검사한다. 조작된 추출 텍스트나 OCR 오류의 의미 검증은 못 한다.
- decimal_sum: values(숫자 문자열 배열), expected(숫자 문자열). 부동소수점 오차 없이 합계를 재계산한다. 입력 수치의 출처는 별도 source_quote 검사와 원본 대조로 검증한다.
- equals: actual, expected. JSON 값의 일치만 검사한다.
- manual: reason. 항상 unverified. 외부 서비스 실호출·의미 검증·육안 확인을 대신하지 않는다.

빈 checks 또는 모르는 type은 unverified, 누락 근거/변경 원본/경로 이탈/계산 불일치는 fail. 종료 코드는 pass=0, fail=1, unverified 또는 잘못된 케이스=2. 원본을 수정해 재실행할 때 새 보고서 경로를 쓴다. 결과물은 검사 전부 통과와 정답 보장을 구분해야 한다.

사람 검토 보고서에는 requirement_id, 원본 위치, 수행한 검사, 기대값/관측값, 상태, 실패 영향, 미검증 이유를 적는다. 요구사항 자체가 빠진 CASE는 자동 검출할 수 없으므로 원래 요구사항 목록과 ID 집합을 직접 대조한다. 모순(예: 두 자료의 다른 날짜)은 하나를 임의 선택하지 않고 추가 요구사항/질문으로 남긴다.
