import os
import shutil
from datetime import datetime
from pathlib import Path

from audio2text import Audio2Text


def load_or_transcribe(audio_folder="audios", title=None) -> dict:
    mom_title = (
        f"{title}.txt"
        if title
        else f"{datetime.isoformat(datetime.now())}.txt"
    )
    text_file_path = Path(f"texts/{mom_title}")

    if text_file_path.exists():
        with open(text_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        parts = content.strip().split(" \n\n")

        return {"file": str(text_file_path), "content": " | ".join(parts)}

    text_file_path.parent.mkdir(parents=True, exist_ok=True)
    text_file_path.touch(exist_ok=True)

    EXCLUDE_FILES = os.getenv("EXCLUDE_AUDIO_FILES", "audio_test.ogg").split(",")

    audio_files = [
        file
        for file in os.listdir(audio_folder)
        if os.path.isfile(os.path.join(audio_folder, file))
        and file not in EXCLUDE_FILES
    ]

    parts = []

    for file in audio_files:
        text = Audio2Text(f"{audio_folder}/{file}")
        transcription = text.transcribe()
        text.write_to_file(str(text_file_path))
        parts.append(transcription.strip())

    chunks_folder = Path(audio_folder) / "chunks"
    if chunks_folder.exists():
        shutil.rmtree(chunks_folder)

    return {"file": str(text_file_path), "content": " | ".join(parts)}
