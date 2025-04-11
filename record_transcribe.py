import os
from recorder_module import record_audio
import whisper

# ✅ Ensure FFmpeg path (edit this if it's elsewhere)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# ✅ Step 1: Record Audio
print("🎤 Starting audio recording...")
audio_path = record_audio(duration=10)  # shorter duration for quick test

if not os.path.exists(audio_path):
    raise FileNotFoundError(f"❌ Audio file not found at {audio_path}")
print(f"✅ Audio recorded and saved at: {audio_path}")

# ✅ Step 2: Load Whisper Model
print("📥 Loading Whisper model (base)...")
model = whisper.load_model("base")

# ✅ Step 3: Transcribe Audio
print("📝 Transcribing audio...")
result = model.transcribe(audio_path)

transcript = result.get("text", "").strip()
if not transcript:
    raise ValueError("❌ No text transcribed. Check audio quality or format.")

# ✅ Step 4: Save Transcription
output_path = "transcription.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(transcript)

print(f"✅ Transcription saved to {output_path}")
print("\n🗣️ TRANSCRIPTION PREVIEW:\n", transcript[:200], "..." if len(transcript) > 200 else "")
