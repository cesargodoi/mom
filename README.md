# Minutes of Meeting (MoM)

Este projeto automatiza o processo de criação de atas de reunião (ATAs) a partir de arquivos de áudio. Ele utiliza técnicas de processamento de áudio para transcrição e agentes de Inteligência Artificial para transformar o texto bruto em documentos formais, estruturados e bem escritos.

## Funcionalidades

- **Transcrição com Faster-Whisper:** Converte áudio em texto usando modelos Whisper otimizados (funciona offline, sem dependência de API).
- **Recuperação Inteligente:** Verifica se a transcrição já existe na pasta `texts/` antes de iniciar um novo processamento.
- **Cache de Modelos:** Modelos Whisper são baixados e reutilizados entreexecuções.
- **Agente de IA com Ferramentas:** Utiliza o framework **Agno** com suporte a ferramentas customizadas.
- **Formatação Humanizada:** Gera documentos em Markdown seguindo regras rigorosas de linguagem natural.
- **Interface CLI Simples:** Solicita título e assinatura via terminal.

## Estrutura de Pastas

```
├── audios/           # Arquivos de áudio de entrada
├── texts/           # Transcrições em cache
├── moms/            # Atas geradas em Markdown
├── tests/           # Testes automatizados
│   └── fixtures/     # Dados de teste
├── models/          # Modelos Whisper (baixados automaticamente)
└── main.py         # Entry point
```

## Tecnologias

- **Python 3.14+**
- **Agno:** Framework para agentes de IA
- **Groq:** LLM Llama 3 para geração de atas
- **Faster-Whisper:** Transcrição de áudio offline
- **Pydub:** Processamento de áudio (requer FFmpeg)

## Pré-requisitos

### FFmpeg

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Instalação

```bash
# Clonar repositório
git clone <url>
cd mom

# Instalar dependências
uv sync

# Ativar ambiente virtual
source .venv/bin/activate
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
HF_TOKEN=seu_token_hugging_face_aqui
GROQ_API_KEY=seu_token_groq_aqui
```

> **Importante:** O `HF_TOKEN` é necessário para descargar modelos Whisper do Hugging Face com maior velocidade. Obtenha um token em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

### Obter Tokens

1. **Hugging Face** (para modelos Whisper):
   - https://huggingface.co/settings/tokens
   - Selecione "New token" com role "Read"

2. **Groq** (para LLM):
   - https://console.groq.com/keys
   - Crie uma nova API key

## Como Usar

1. Coloque arquivos de áudio (`.mp3`, `.ogg`, `.wav`, `.m4a`) na pasta `audios/`
2. Execute:
   ```bash
   uv run python main.py
   ```
3. Informe o título e assinatura da ATA
4. A ATA será gerada em `moms/<titulo>.md`

## Testes

```bash
uv run pytest tests/ -v
```

Cobertura atual: **99%**

## Padrão da ATA Gerada

- Título, Data, Horário e Local
- Lista de Participantes
- Seção "O que nós refletimos"
- Problemas encontrados (se aplicável)
- Resumo do clima e assinatura