# Minutes of Meeting (MoM) 🎙️📝

Este projeto automatiza o processo de criação de atas de reunião (ATAs) a partir de arquivos de áudio. Ele utiliza técnicas de processamento de áudio para transcrição e agentes de Inteligência Artificial para transformar o texto bruto em documentos formais, estruturados e bem escritos.

## 🚀 Funcionalidades

- **Transcrição Segmentada:** Divide arquivos de áudio grandes em "chunks" menores para garantir uma transcrição estável e eficiente via Google Web Speech API.
- **Recuperação Inteligente:** Verifica se a transcrição já existe na pasta `texts/` antes de iniciar um novo processamento, otimizando o tempo de execução.
- **Agente de IA com Ferramentas:** Utiliza o framework **Agno** com suporte a ferramentas customizadas para extração de contexto e geração de atas.
- **Formatação Humanizada:** Gera documentos em Markdown seguindo regras rigorosas de linguagem natural, evitando termos robóticos.
- **Gestão de Artefatos:** Organiza automaticamente os arquivos em pastas separadas:
  - `audios/`: Local para colocar os arquivos de entrada.
  - `texts/`: Armazena as transcrições brutas para referência futura.
  - `moms/`: Destino final das atas geradas em Markdown.
- **Interface CLI Simples:** Solicita informações básicas como título e assinatura via terminal.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Agno:** Framework para criação de agentes de IA baseados em ferramentas.
- **OpenAI/Groq:** LLMs de última geração (GPT-4/Llama 3) para processamento semântico.
- **SpeechRecognition:** Para conversão de áudio em texto.
- **Pydub:** Para manipulação e segmentação de arquivos de áudio (requer FFmpeg).
- **Python-dotenv:** Para gerenciamento de variáveis de ambiente.

## 📋 Pré-requisitos

Antes de executar o projeto, você precisará ter o **FFmpeg** instalado no seu sistema para que a biblioteca `pydub` possa processar os áudios.

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## 🔧 Instalação e Configuração

1. Clone o repositório:
   ```bash
   git clone <url-do-seu-repositorio>
   cd mom
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   *(Caso não tenha um requirements.txt, instale: `pip install agno openai groq pydub SpeechRecognition python-dotenv`)*

3. Configure suas chaves de API:
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   GROQ_API_KEY=seu_token_aqui
   # Caso prefira OpenAI:
   # OPENAI_API_KEY=seu_token_aqui
   ```

## 📖 Como Usar

1. Coloque seus arquivos de áudio (ex: `.mp3`, `.wav`, `.m4a`) dentro da pasta `audios/`.
2. Execute o script principal:
   ```bash
   python main.py
   ```
3. Responda às perguntas no terminal:
   - **Qual o título da Ata?** (Ex: Reunião de Planejamento Mensal)
   - **Quem assina a Ata?** (Seu Nome ou Nome do Secretário)
4. O sistema irá transcrever os áudios, processar via IA e salvar o resultado final em `moms/titulo-da-ata.md`.

## 📄 Estrutura do Documento Gerado

A ata gerada segue o padrão:
- Título, Data, Horário e Local.
- Lista de Participantes e Ausências.
- Seção "O que nós refletimos" (com linguagem descritiva e anonimizada).
- Problemas encontrados (seção condicional para conflitos interpessoais).
- Resumo do clima da reunião e assinatura.