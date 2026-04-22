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

    def test_audio2text_init(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        with patch("audio2text.get_model") as mock_get_model:
            mock_model = MagicMock()
            mock_get_model.return_value = mock_model

            converter = Audio2Text(str(audio_path))

        assert converter.input_path == str(audio_path)
        assert converter.audio_name == "audio_test"

    def test_audio2text_model_cache(self):
        with patch("audio2text.get_model") as mock_get_model:
            mock_model = MagicMock()
            mock_get_model.return_value = mock_model

            converter = Audio2Text("test.ogg")

        assert converter.model is mock_model

    def test_audio2text_transcribe(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        with patch("audio2text.get_model") as mock_get_model:
            mock_model = MagicMock()
            mock_segment = MagicMock()
            mock_segment.text = "Transcribed text"
            mock_model.transcribe.return_value = ([mock_segment], None)
            mock_get_model.return_value = mock_model

            converter = Audio2Text(str(audio_path))
            result = converter.transcribe()

        assert isinstance(result, str)
        assert "Transcribed text" in result

    def test_audio2text_transcribe_empty(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        with patch("audio2text.get_model") as mock_get_model:
            mock_model = MagicMock()
            mock_model.transcribe.return_value = ([], None)
            mock_get_model.return_value = mock_model

            converter = Audio2Text(str(audio_path))
            result = converter.transcribe()

        assert result == ""

    def test_audio2text_transcribe_multiple_segments(self):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        with patch("audio2text.get_model") as mock_get_model:
            mock_model = MagicMock()
            seg1 = MagicMock(text="Primeiro texto")
            seg2 = MagicMock(text="Segundo texto")
            mock_model.transcribe.return_value = ([seg1, seg2], None)
            mock_get_model.return_value = mock_model

            converter = Audio2Text(str(audio_path))
            result = converter.transcribe()

        assert "Primeiro texto" in result
        assert "Segundo texto" in result

    def test_audio2text_write_to_file(self, tmp_path):
        audio_path = FIXTURE_DIR / "audio_test.ogg"
        if not audio_path.exists():
            pytest.skip("audio_test.ogg not found")

        output_file = tmp_path / "output.txt"

        with patch("audio2text.get_model") as mock_get_model:
            mock_model = MagicMock()
            mock_get_model.return_value = mock_model

            converter = Audio2Text(str(audio_path))
            converter.full_text = "Test transcription"
            converter.write_to_file(str(output_file))

        assert output_file.exists()
        assert output_file.read_text() == "Test transcription\n\n"


class TestGetModel:
    def test_get_model_creates_model(self):
        with patch("audio2text.WhisperModel") as mock_whisper:
            mock_model = MagicMock()
            mock_whisper.return_value = mock_model

            from audio2text import get_model
            result = get_model("small")

        mock_whisper.assert_called_once()

    def test_get_model_caches(self):
        from audio2text import _model_cache

        with patch("audio2text.WhisperModel") as mock_whisper:
            mock_model = MagicMock()
            mock_whisper.return_value = mock_model

            _model_cache.clear()

            from audio2text import get_model
            get_model("base")
            get_model("base")

        assert mock_whisper.call_count == 1