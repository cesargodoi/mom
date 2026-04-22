import pytest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from audio2text import Audio2Text

FIXTURE_DIR = Path(__file__).parent / "fixtures"


class TestAudio2Text:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        chunks_dir = FIXTURE_DIR / "chunks"
        if chunks_dir.exists():
            shutil.rmtree(chunks_dir)

    def test_audio2text_init(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        converter = Audio2Text(str(audio_path))

        assert converter.input_path == str(audio_path)
        assert converter.audio_name == "audio_test"

    def test_audio2text_chunk_length(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        converter = Audio2Text(str(audio_path))

        assert converter.chunk_length_ms == 30_000

    def test_audio2text_split_audio_creates_chunks(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        converter = Audio2Text(str(audio_path))

        chunk_dir = audio_path.parent / "chunks" / "audio_test"
        assert chunk_dir.exists()

    def test_audio2text_transcribe(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        converter = Audio2Text(str(audio_path))
        result = converter.transcribe()

        assert isinstance(result, str)

    def test_audio2text_transcribe_unknown_value(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"

        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        import speech_recognition as sr

        with patch("audio2text.sr.Recognizer") as mock_recognizer, \
             patch("audio2text.sr.AudioFile"):
            mock_rec = MagicMock()
            mock_rec.record.return_value = MagicMock()
            mock_rec.recognize_google.side_effect = sr.UnknownValueError()
            mock_recognizer.return_value = mock_rec

            converter = Audio2Text(str(audio_path))
            result = converter.transcribe()

            assert "[inaudível]" in result

    def test_audio2text_transcribe_request_error(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"

        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        import speech_recognition as sr

        with patch("audio2text.sr.Recognizer") as mock_recognizer, \
             patch("audio2text.sr.AudioFile"):
            mock_rec = MagicMock()
            mock_rec.record.return_value = MagicMock()
            mock_rec.recognize_google.side_effect = sr.RequestError("Error")
            mock_recognizer.return_value = mock_rec

            converter = Audio2Text(str(audio_path))
            result = converter.transcribe()

            assert "[erro:" in result

    def test_audio2text_write_to_file(self, tmp_path):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        output_file = tmp_path / "output.txt"

        with patch("audio2text.AudioSegment"):
            converter = Audio2Text(str(audio_path))
            converter.full_text = "Test transcription"
            converter.write_to_file(str(output_file))

        assert output_file.exists()
        assert output_file.read_text() == "Test transcription\n\n"