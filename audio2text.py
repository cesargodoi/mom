from pathlib import Path

from faster_whisper import WhisperModel

_model_cache = {}


def get_model(size: str = "small") -> WhisperModel:
    if size not in _model_cache:
        _model_cache[size] = WhisperModel(
            size, device="cpu", compute_type="int8", download_root="models"
        )
    return _model_cache[size]


class Audio2Text:
    def __init__(self, input_path: str, model_size: str = "small"):
        self.input_path = input_path
        self.audio_name = Path(input_path).stem
        self.model = get_model(model_size)
        self.full_text = ""

    def transcribe(self) -> str:
        print(f"- {self.audio_name} ", end="", flush=True)

        segments, _ = self.model.transcribe(
            self.input_path, language="pt", vad_filter=True
        )

        text_parts = []
        for segment in segments:
            print(".", end="", flush=True)
            text_parts.append(segment.text)

        self.full_text = " ".join(text_parts)
        print()
        return self.full_text

    def write_to_file(self, text_file_path: str):
        with open(text_file_path, "a") as f:
            f.write(f"{self.full_text}\n\n")
