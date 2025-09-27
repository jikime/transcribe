#!/usr/bin/env python3
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python transcribe.py <audio_file>")
    sys.exit(1)

audio_path = Path(sys.argv[1])
if not audio_path.exists():
    print("File not found:", audio_path)
    sys.exit(1)

out_txt = Path("transcript.txt")
out_srt = Path("transcript.srt")

# Try faster-whisper first, then fallback to openai-whisper
try:
    from faster_whisper import WhisperModel
    print("Using faster-whisper...")
    model_size = "small"  # 필요하면 "medium" 등으로 변경
    model = WhisperModel(model_size, device="auto", compute_type="auto")
    segments, info = model.transcribe(str(audio_path), beam_size=5)
    full_text = []
    srt_lines = []
    idx = 1
    for seg in segments:
        start = seg.start
        end = seg.end
        text = seg.text.strip()
        full_text.append(text)
        # SRT time format helper
        def fmt(t):
            h = int(t // 3600)
            m = int((t % 3600) // 60)
            s = int(t % 60)
            ms = int((t - int(t)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        srt_lines.append(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{text}\n")
        idx += 1
    transcript = "\n".join(full_text)
    out_txt.write_text(transcript, encoding="utf-8")
    out_srt.write_text("\n".join(srt_lines), encoding="utf-8")
    print("Transcript saved to:", out_txt)
    print("SRT saved to:", out_srt)
except Exception as e_fw:
    print("faster-whisper failed or not available:", e_fw)
    print("Trying OpenAI whisper fallback...")
    try:
        import whisper
        model = whisper.load_model("small")
        print("Loaded whisper model 'small' (may be slower). Transcribing...")
        result = model.transcribe(str(audio_path))
        text = result.get("text", "").strip()
        out_txt.write_text(text, encoding="utf-8")
        # simple SRT: split by sentences (naive)
        import re
        sentences = re.split(r'(?<=[\.\?\!])\s+', text)
        srt_lines = []
        cur = 0.0
        dur = result.get("language")  # not reliable for timing
        # We won't produce accurate timings in fallback; produce plain transcript
        out_srt.write_text("", encoding="utf-8")
        print("Transcript saved to:", out_txt)
        print("Note: SRT timings not generated for whisper fallback.")
    except Exception as e_wh:
        print("Both transcription methods failed. Error details:")
        print("faster-whisper error:", e_fw)
        print("whisper error:", e_wh)
        print("\nSuggestions:")
        print(" - Ensure ffmpeg is installed.")
        print(" - Try installing faster-whisper or openai whisper as shown in README.")
        print(" - If you prefer, upload an audio-only WAV/MP3 here so I can try transcribing again.")

