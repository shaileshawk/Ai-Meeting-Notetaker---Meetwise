import os
import streamlit as st
import whisper
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import openai
from dotenv import load_dotenv
from main import join_google_meet

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# UI Title
st.title("🎙️ Meetwise AI - Meeting Transcriber & Summarizer")

# Text input for meeting link
meeting_link = st.text_input("🔗 Paste your Google Meet / Zoom / Teams link here:")

# Recording duration selector
duration = st.slider("🎛️ Select recording duration (seconds):", 10, 120, 30)

# Function to record and transcribe
def record_and_process_audio(duration):
    with st.spinner("🎙️ Recording audio..."):
        samplerate = 44100
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='float32')
        sd.wait()
        mono = np.mean(recording, axis=1)
        os.makedirs("assets", exist_ok=True)
        filename = f"assets/recording_{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav"
        write(filename, samplerate, mono)
        st.success(f"✅ Audio recorded and saved to: {filename}")
    return filename

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    with st.spinner("🧠 Transcribing with Whisper..."):
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        transcript = result["text"]
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        st.text_area("📝 Transcription", transcript, height=200)
    return transcript

# Function to summarize using OpenAI
def summarize_with_gpt(transcript):
    with st.spinner("🤖 Generating summary and tasks via GPT..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a smart assistant that listens to meeting transcripts and generates summaries and to-do lists."},
                {"role": "user", "content": f"Here's the meeting transcript:\n{transcript}\n\nPlease provide a summary and action items."}
            ]
        )
        ai_output = response['choices'][0]['message']['content']
        with open("summary_and_tasks.txt", "w", encoding="utf-8") as f:
            f.write(ai_output)
        st.text_area("📌 Summary & Tasks", ai_output, height=200)
        st.success("✅ Summary and transcription saved!")

# 🔘 Button 1: Manual recording
if st.button("🎤 Start Recording & Transcribe"):
    audio_file = record_and_process_audio(duration)
    transcript = transcribe_audio(audio_file)
    summarize_with_gpt(transcript)

# 🔘 Button 2: Join meeting and record
if st.button("🧑‍💻 Join Meeting & Record"):
    if not meeting_link.strip():
        st.warning("⚠️ Please paste a meeting link before joining.")
    else:
        st.success("✅ Bot is joining the meeting in your Chrome browser...")
        join_google_meet(meeting_link)
        st.info("⏳ Waiting 15 seconds to let the meeting load fully...")
        time.sleep(15)
        
        st.info("🎙️ Starting audio recording now...")
        audio_file = record_and_process_audio(duration)

        st.info("🧠 Transcribing the recording...")
        transcript = transcribe_audio(audio_file)

        st.info("🧾 Summarizing the meeting...")
        summarize_with_gpt(transcript)

        st.success("✅ All done! You can download your transcript and summary below.")


# 📥 Download buttons
if os.path.exists("transcription.txt"):
    with open("transcription.txt", "r", encoding="utf-8") as f:
        st.download_button("📥 Download Transcription", f, file_name="transcription.txt")

if os.path.exists("summary_and_tasks.txt"):
    with open("summary_and_tasks.txt", "r", encoding="utf-8") as f:
        st.download_button("📥 Download Summary & Tasks", f, file_name="summary_and_tasks.txt")