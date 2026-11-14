from pathlib import Path
from faster_whisper import WhisperModel

_model = None


def get_model(size: str = "base.en") -> WhisperModel:
    """Load once, reuse afterwards (loading is slow)."""
    global _model
    if _model is None:
        _model = WhisperModel(size, device="cpu", compute_type="int8")
    return _model


def transcribe(audio_path: Path) -> list[dict]:
    segments, _ = get_model().transcribe(
        str(audio_path),
        language="en",
        word_timestamps=True,
        beam_size=5,
        # Do NOT pass the target paragraph as initial_prompt:
        # it biases Whisper toward the target and hides real mistakes.
    )
    words = []
    for seg in segments:
        for w in seg.words:
            words.append({
                "word": w.word.strip(),
                "start": round(w.start, 2),
                "end": round(w.end, 2),
                "confidence": round(w.probability, 3),
            })
    return words