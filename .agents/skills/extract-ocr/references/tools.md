# 로컬 도구와 좌표

설치는 루트 docs/setup.md 참조. `tesseract --list-langs`로 kor/eng 존재 확인. 실행 예:

```text
tesseract page.png page -l kor+eng --psm 3 tsv
pdftoppm -r 300 -png scan.pdf page
```

PSM 3은 자동 배치, 6은 단일 균일 블록이다. 단어 TSV의 left/top/width/height/conf를 보존한다. PDF 페이지 번호는 1부터 시작한다. 이미지 좌표 원점은 왼쪽 위다. CLI JSON source_sha256은 이미지 해시이며 PDF 원본은 별도 매핑한다.

타일 예: 2400px 높이 이미지에 [0,1300), [1100,2400) 두 영역을 사용하면 겹침은 200px이다. 각 결과에 crop_origin=(x,y), scale, rotation을 기록한다. 무회전 이미지라면 원본 좌표=(타일 좌표/scale)+crop_origin. 회전 시 역변환 행렬을 사용한다. 같은 숫자가 다른 행에 반복될 수 있으므로 텍스트만으로 중복 제거하지 않는다. 전체 이미지도 별도로 읽어 경계 누락을 점검한다.

전환 기준: 표본의 필수 필드 하나라도 판독 불가/불일치이면 재검토. 인쇄문 Tesseract → 전처리/PSM 변경 → 설치된 다른 OCR 또는 사용 가능 비전 도구 → 사람 확인. 손글씨/병합표는 일찍 대체 경로를 택한다. 번역 결과를 원문 필드에 덮어쓰지 않는다. 민감 후보 자동 표시로 모든 이름/날짜를 찾을 수는 없다.
