import pytest
import os
import shutil
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from services import load_or_transcribe


FIXTURE_DIR = Path(__file__).parent / "fixtures"


class TestLoadOrTranscribe:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_load_or_transcribe_with_existing_cache(self):
        text_dir = Path("texts")
        text_dir.mkdir(parents=True, exist_ok=True)
        fixture = FIXTURE_DIR / "text_test.txt"
        text_file = text_dir / "text_test.txt"
        text_file.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

        result = load_or_transcribe(title="text_test")

        assert "content" in result
        assert "file" in result
        assert "transcription de teste" in result["content"]

    def test_load_or_transcribe_no_audio_files(self):
        audio_dir = Path("audios")
        audio_dir.mkdir(parents=True, exist_ok=True)

        result = load_or_transcribe(title="empty_test", audio_folder="audios")

        assert "content" in result
        assert "file" in result
        assert result["content"] == ""

    def test_load_or_transcribe_with_real_audio(self):
        audio_dir = Path("audios")
        audio_dir.mkdir(parents=True, exist_ok=True)

        result = load_or_transcribe(title="integration_test", audio_folder="audios")

        assert "content" in result
        assert "file" in result

    def test_load_or_transcribe_title_generation(self):
        audio_dir = Path("audios")
        audio_dir.mkdir(parents=True, exist_ok=True)

        result = load_or_transcribe(audio_folder="audios")

        assert "file" in result

    def test_load_or_transcribe_with_audio_in_temp_dir(self):
        temp_path = Path(self.temp_dir)
        audio_dir = temp_path / "audios"
        audio_dir.mkdir(parents=True, exist_ok=True)
        chunks_dir = audio_dir / "chunks"
        chunks_dir.mkdir(parents=True, exist_ok=True)
        (chunks_dir / "dummy.txt").touch()

        audio_file = audio_dir / "real_audio.ogg"
        audio_file.write_bytes((FIXTURE_DIR / "audio_test.ogg").read_bytes())

        result = load_or_transcribe(title="temp_test", audio_folder=str(audio_dir))

        assert "content" in result
        assert "file" in result
        assert not chunks_dir.exists()