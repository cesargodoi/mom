import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
import tempfile
import os
import shutil

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import get_prompt, save_markdown, clean_markdown, get_text, main


class TestGetPrompt:
    def test_get_prompt_existing(self):
        prompt = get_prompt("circle_meeting")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_get_prompt_not_found(self):
        with pytest.raises(FileNotFoundError):
            get_prompt("nonexistent_prompt")


class TestSaveMarkdown:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_save_markdown_with_title(self, tmp_path):
        content = "# Test ATA"
        result = save_markdown(content, folder=str(tmp_path), title="test_ata")
        assert result.exists()
        assert result.read_text(encoding="utf-8") == content

    def test_save_markdown_without_title(self, tmp_path):
        content = "# Test ATA"
        result = save_markdown(content, folder=str(tmp_path))
        assert result.exists()
        assert result.name.endswith(".md")

    def test_save_markdown_creates_folder(self, tmp_path):
        content = "# Test ATA"
        nested_path = tmp_path / "subfolder"
        result = save_markdown(content, folder=str(nested_path), title="test")
        assert result.exists()
        assert nested_path.exists()


class TestCleanMarkdown:
    def test_clean_markdown_with_fenced_code(self):
        text = "```markdown\n# Conteúdo\n```"
        result = clean_markdown(text)
        assert result == "# Conteúdo"

    def test_clean_markdown_without_fenced_code(self):
        text = "# Conteúdo normal"
        result = clean_markdown(text)
        assert result == "# Conteúdo normal"

    def test_clean_markdown_empty(self):
        assert clean_markdown("") == ""

    def test_clean_markdown_with_triple_backticks(self):
        text = "```\n conteudo \n```"
        result = clean_markdown(text)
        assert "```" not in result


class TestMain:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_main_with_mocked_agent(self):
        with patch("builtins.input", side_effect=["Test Title", "John Doe"]), \
             patch("main.Agent") as mock_agent_class, \
             patch("main.get_prompt") as mock_prompt, \
             patch("main.load_or_transcribe") as mock_load:
            mock_load.return_value = {"file": "test.txt", "content": "Reunião aconteceu"}
            mock_agent = MagicMock()
            mock_response = MagicMock()
            mock_response.content = "# ATA de Reunião\n\nAssinatura: John Doe"
            mock_agent.run.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            mock_prompt.return_value = "Prompt de teste"

            with patch("main.save_markdown") as mock_save:
                mock_save.return_value = Path("moms/test.md")
                result = main()

                mock_agent.run.assert_called_once()
                assert mock_save.called

    def test_main_with_output_attribute(self):
        with patch("builtins.input", side_effect=["Title", "Signer"]), \
             patch("main.Agent") as mock_agent_class, \
             patch("main.get_prompt") as mock_prompt, \
             patch("main.load_or_transcribe") as mock_load:
            mock_load.return_value = {"file": "test.txt", "content": "Content"}
            mock_agent = MagicMock()
            mock_response = MagicMock(spec=[])
            mock_response.output = "# Ata"
            del mock_response.content
            mock_agent.run.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            mock_prompt.return_value = "Prompt"

            with patch("main.save_markdown") as mock_save:
                mock_save.return_value = Path("moms/title.md")
                main()

                assert mock_save.called