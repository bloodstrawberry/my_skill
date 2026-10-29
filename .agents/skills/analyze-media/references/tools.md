# 미디어 도구 절차

도구 설치/인증은 docs/setup.md에서 별도 관리한다. 다음 명령은 외부 API를 호출하지 않는다.

```text
ffprobe -v error -show_format -show_streams -of json input.mp4
ffmpeg -i input.mp4 -ss 295 -t 300 -vn -ar 16000 -ac 1 chunk-001.wav
ffmpeg -i input.mp4 -ss 312.5 -frames:v 1 frame-312_5.png
whisper chunk-001.wav --model SELECTED_MODEL --output_format json --output_dir transcript
```

SELECTED_MODEL은 실제 설치 모델로 바꾼다. 명령을 그대로 실행하기 전 입력 경로와 기존 출력 충돌을 확인한다. FFmpeg는 `-n`을 추가해 덮어쓰기를 막는다. `-ss`를 입력 뒤에 두어 디코딩 후 시점을 선택하며 실제 결과 길이를 ffprobe로 재확인한다. 비정상 시작 시각·가변 프레임레이트에서는 실제 PTS와 상대 초 대응을 남긴다. 라이브 스트림의 날짜/시간대는 메타데이터가 없으면 unknown이다.

segments.py의 계획은 초 단위 0부터 [start,end) 구간이다. overlap < chunk. 전사 JSON에는 source, source_sha256, chunk_id, offset_seconds, start_seconds, end_seconds, speaker_label, speaker_uncertain, raw_text, unclear_spans를 기록한다. ASR 출력 구간의 시작/끝에 offset을 더하고 chunk 길이를 벗어난 타임스탬프는 오류로 표시한다.

성능/정확도는 이 저장소가 벤치마크하지 않았다. 모델 다운로드는 네트워크와 디스크가 필요하며, Whisper의 실제 한국어 인식과 화자 분리는 별도 검증 대상이다. 원격 ASR 사용 시 해당 서비스의 현재 공식 API 문서와 동의된 업로드 정책을 먼저 확인하고 실제 호출/모의 결과를 구분한다.
