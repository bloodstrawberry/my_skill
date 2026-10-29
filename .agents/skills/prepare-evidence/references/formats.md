# 형식과 위치 계약

`prepare.py`는 Python 3.10+와 표준 라이브러리로 UTF-8 TXT/MD/JSON/CSV/TSV를 처리한다. UTF-8이 아니면 오류를 보존하고 확인된 인코딩으로 별도 사본을 변환한다. CSV row는 논리 레코드 번호이며 여러 줄 셀의 물리 줄 번호와 다르다.

| 형식 | 선택 도구 | 위치 / 한계 |
|---|---|---|
| PDF | pypdf | 1부터 시작하는 page. 이미지 속 글자는 추출 불가. 빈 페이지도 OCR 필요 후보이며 렌더링 대조 필요 |
| DOCX | python-docx | paragraph 또는 table/row. 고정 페이지 없음. 머리글·텍스트박스·중첩표 등 별도 확인 |
| XLSX/XLSM | openpyxl | sheet/cell. 숨김 시트 포함, 수식 보존, 실행·재계산 안 함 |
| PNG/JPEG/스캔 | extract-ocr | 원본 크기·page·bbox와 좌표 변환을 별도 기록 |
| MP3/WAV/MP4 | analyze-media | 원본 초 단위 구간과 시간대(있는 경우) |
| HWP/HWPX/구형 DOC/XLS/PPT/암호화 파일 | 설치된 전용 도구 또는 수동 내보내기 | 원본과 내보내기 대응표 유지. 지원된 척하지 않기 |

`manifest.json`: schema_version, source_root, generated_at(UTC), filesystem_time_zone, python, files[], missing[], issues[]. 각 파일은 path, sha256, bytes, mtime_utc, status, issues, tool, units와 선택적 duplicate_of를 가진다. 읽기 실패 시 일부 필드는 없을 수 있다.
`evidence.json`: units[]의 id, source(원본 상대 경로), source_sha256, location, text. 파일 시스템 수정 시각은 내용에 등장한 날짜/시간대와 다르다. 문서 내부 시간대가 불명확하면 추정하지 않는다.

큰 파일은 해시는 스트리밍하지만 추출은 메모리를 사용한다. 예산을 초과하면 자료를 분할한 사본과 원본 위치 매핑을 사용한다. 원본 폴더 안에 비밀 파일을 두지 않는다. 링크는 건너뛰며 암호화 해제·매크로 실행·외부 업로드는 자동 수행하지 않는다.
