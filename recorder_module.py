import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
from datetime import datetime

def record_audio(duration=15, samplerate=44100):
    import sounddevice as sd
    import numpy as np
    import os
    from scipy.io.wavfile import write
    from datetime import datetime

    print("🎙️Recording started...")

    try:
        sd.default.device = None  # remove this line if you want to try a specific index
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='float32')
        sd.wait()
        print("✅ Recording complete")

        mono = np.mean(recording, axis=1)
        os.makedirs("assets", exist_ok=True)
        filename = f"assets/recording_{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav"
        write(filename, samplerate, mono)
        print(f"✅ File saved: {filename}")
        return filename

    except Exception as e:
        print("❌ Error while recording:", e)
if __name__ == "__main__":
    record_audio()
