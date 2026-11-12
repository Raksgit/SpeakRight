import sounddevice as sd
import soundfile as sf
import os
from pathlib import Path

# Audio configuration
SAMPLE_RATE = 16000
DURATION = 5
CHANNELS = 1

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Audio storage directory
OUTPUT_DIR = BASE_DIR / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "recorded_audio.wav"


def record_audio():

    print("\nWelcome to SpeakRight!")
    print("Get ready to record your voice.")

    try:
        print("\nRecording started... Speak now!")

        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32"
        )

        sd.wait()

        print("Recording completed!")

        sf.write(OUTPUT_FILE, audio, SAMPLE_RATE)

        print(f"Audio saved successfully: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Recording failed: {e}")


if __name__ == "__main__":
    record_audio()