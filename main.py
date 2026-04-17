from datetime import datetime
from pathlib import Path

from agno.agent import Agent

# from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv

from audio2text import run_transcription
from instructions import circle_meeting

load_dotenv()


def save_markdown(
    content: str, folder: str = "moms", title: str = None, assign: str = "---"
) -> Path:
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    filename = (
        f"{title}.md" if title else f"{datetime.isoformat(datetime.now())}.md"
    )
    file_path = folder_path / filename

    file_path.write_text(content, encoding="utf-8")

    return file_path


def clean_markdown(text: str) -> str:
    if text.startswith("```"):
        return text.strip("```markdown").strip("```").strip()  # noqa: PLE1310
    return text


@tool
def transcribe_audios(audio_folder: str = "audios", title: str = "") -> dict:
    """
    Transcribe all audio files inside the 'audios' folder
    and return the transcriptions
    """
    return run_transcription(audio_folder=audio_folder, title=title)


def main():
    print(" Minutes of Meeting ".center(80, "."))
    title = input("Qual o título da Ata? ")
    assign = input("Quem assina a Ata? ")

    agent = Agent(
        id="mom",
        name="Minutes of Meeting",
        role="Elabore uma ATA baseada no texto extraído de um áudio",
        instructions=circle_meeting,
        # model=Groq(id="llama-3.3-70b-versatile", temperature=0.7),
        model=OpenAIChat(id="gpt-5.4-nano", temperature=0.7),
        tools=[transcribe_audios],
    )

    response = agent.run(
        f"""
        Use a ferramenta transcribe_audios, usando o titulo: "{title.strip()}".
        Depois gere uma ATA DE REUNIÃO em markdown usando a assinatura: 
        "{assign.strip()}".
        """
    )

    content = getattr(response, "content", None) or getattr(
        response, "output", ""
    )

    content = clean_markdown(content)

    return save_markdown(content, title=title.strip())


if __name__ == "__main__":
    main()
