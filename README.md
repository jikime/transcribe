1) 준비물
Python 3.8+ (권장)
ffmpeg 설치 : brew install ffmpeg
가상환경(uv) 설치
-curl -LsSf https://astral.sh/uv/install.sh | sh
프로젝트 생성
- uv init transcribe
- cd transcribe & uv venv -p 3.12
- source .venv/bin/activate
2) 필요한 패키지 설치
- uv add faster-whisper ffmpeg-python

3) mp4 → wav 오디오 추출
ffmpeg -i "다운로드파일.mp4" -vn -ac 1 -ar 16000 -y "input_audio.wav"
-ac 1 : mono (모델 안정성 위해 권장)
-ar 16000 : 샘플레이트 16kHz (작업환경에 따라 16k/24k 권장)

4) 실행 가능한 파이썬 스크립트
uv run transcribe.py input_audio.wav

5) 결과 파일
transcript.txt : 전체 지문(순수 텍스트)
transcript.srt : 자막(구간별 텍스트)
