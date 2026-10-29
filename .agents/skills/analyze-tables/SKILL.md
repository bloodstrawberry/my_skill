---
name: analyze-tables
description: CSV·Excel의 정제, 조인, 집계, 이상치와 수식을 분석해 근거 있는 표 결과가 필요할 때 사용한다.
---

# analyze-tables

## 실행 환경
Cofa 응시에서는 docs/hackathon.md와 AGENTS.md의 대회 제한을 먼저 적용한다. 외부 API/추가 AI 모델은 실행하지 않는다. 다른 대회와 일반 연습은 해당 환경의 허용 범위를 확인한다.

## 입력·출력
입력: 원본 표, 키/단위/기간, 요구사항. 출력: 정제 결과, 변환 기록, 원본 셀/행 매핑, 검증 보고.
## 절차
1. prepare-evidence로 목록·해시를 만들고 pandas/openpyxl 설치를 확인한다.
2. ID·우편번호는 문자열로 읽어 앞자리 0을 보존한다. 인코딩·날짜 형식·시간대·통화·결측 의미를 확인한다.
3. 조인 전에 키 중복과 null을 점검한다. pandas merge의 validate와 indicator로 행 증식/미매칭을 확인한다.
4. 정제 전후 행 수, 유일 키 수, 결측 수, 합계 변화를 기록한다. 이상치를 근거 없이 삭제하지 않는다.
5. 통화는 Decimal 또는 최소 화폐 단위 정수로 계산한다. Excel 수식과 캐시값은 별도로 읽고 openpyxl이 재계산하지 않는다는 점을 표시한다.
6. 중요한 집계는 독립 계산으로 대조하고 경계/빈 집합/중복 사례를 verify-results로 검증한다. 원본 시트·셀/논리 행을 보고서에 연결한다.
## 실패·완료
형식/키 의미가 불명확하면 추측 조인을 멈추고 질문한다. 메모리가 부족하면 필요한 열/청크만 읽는다. 원본 대비 변환 내역과 검증 가능한 결과가 있으면 완료한다.
## 도구 근거
https://pandas.pydata.org/docs/ 및 https://openpyxl.readthedocs.io/ . 자체 작성 지침이며 pandas 공식 Skill로 주장하지 않는다.
