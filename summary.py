import os
from dotenv import load_dotenv
import openai
import whisper
from recorder_module import record_audio

# ✅ Load .env and OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ OPENAI_API_KEY not found!")

# ✅ Record Audio
filename = record_audio(duration=30)

# ✅ Transcribe with Whisper
print("📥 Loading Whisper model...")
model = whisper.load_model("base")
result = model.transcribe(filename)
transcript = result["text"]

# ✅ Save transcription
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print("✅ Transcription saved as transcription.txt")

# ✅ Use OpenAI v1+ Chat API
from openai import OpenAI

client = OpenAI(api_key=openai.api_key)

print("💡 Generating summary and to-dos...")
chat_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a meeting assistant. Read transcripts and give a summary and action points."
        },
        {
            "role": "user",
            "content": f"Transcript:\n{transcript}\n\nGive summary and to-do list."
        }
    ]
)

output = chat_response.choices[0].message.content

# ✅ Save Output
with open("summary_and_tasks.txt", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ Summary and to-dos saved as summary_and_tasks.txt")

# ✅ Auto-open summary in Notepad
import subprocess

try:
    subprocess.Popen(["notepad.exe", "summary_and_tasks.txt"])
    print("📝 summary_and_tasks.txt opened in Notepad!")
except Exception as e:
    print(f"❌ Failed to open Notepad: {e}")
