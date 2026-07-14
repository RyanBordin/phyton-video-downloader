# 🎬 Baixador Multimídia do YouTube

Um script simples e direto em Python para baixar vídeos e playlists do YouTube. O script permite escolher entre baixar apenas o vídeo (MP4) ou apenas o áudio (MP3), organizando playlists automaticamente em pastas dedicadas.

## ✨ Funcionalidades

- **Suporte a Playlists e Vídeos Soltos:** Reconhece automaticamente se o link é de uma playlist ou vídeo individual.
- **Organização Automática:** Playlists são salvas em pastas próprias (com o nome da playlist) dentro do seu diretório `Downloads`.
- **Formatos Suportados:**
  - Vídeo: `MP4` (melhor qualidade de vídeo e áudio combinados).
  - Áudio: `MP3` (extraído e convertido para a qualidade de 192kbps).

## 🚀 Pré-requisitos

Antes de rodar a aplicação, você precisará ter instalado no seu sistema:

- **Python 3.x**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** (Biblioteca principal de download)
- **[FFmpeg](https://ffmpeg.org/)** (Essencial para extração e conversão de áudio para MP3)

## 🛠️ Instalação e Configuração

1. **Clone o repositório (ou baixe o arquivo Python):**
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

2. **Instale a dependência do Python:**
   ```bash
   pip install yt-dlp
   ```

3. **Instale o FFmpeg:**
   - **Windows:** Você pode instalar via [WinGet](https://learn.microsoft.com/pt-br/windows/package-manager/winget/) rodando `winget install ffmpeg` no terminal, ou baixar os binários pelo site oficial.
   - **Linux:** `sudo apt install ffmpeg` (Debian/Ubuntu) ou `sudo pacman -S ffmpeg` (Arch).
   - **macOS:** `brew install ffmpeg`

4. **⚠️ ATENÇÃO: Configuração do caminho do FFmpeg no código**

   No script, o caminho para o executável do FFmpeg está fixo (hardcoded) para um diretório específico do Windows:
   ```python
   'ffmpeg_location': r'C:\Users\[user]\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe',
   ```
   **Para que o script funcione no seu computador, você precisa ajustar isso. Escolha uma das opções:**
   - **Opção 1 (Recomendada):** Se o FFmpeg já estiver adicionado às Variáveis de Ambiente (`PATH`) do seu sistema operacional, você pode simplesmente **remover ou comentar** essa linha no código. O `yt-dlp` o encontrará automaticamente.
   - **Opção 2:** Altere a string `r'C:\...\ffmpeg.exe'` para o caminho absoluto de onde o FFmpeg está instalado na sua máquina atual.

## 💻 Como Usar

1. Execute o script via terminal:
   ```bash
   python nome_do_script.py
   ```
2. Ao ver a mensagem `Cole o link aqui:`, insira a URL do vídeo ou da playlist do YouTube.
3. Em seguida, escolha o formato de saída digitando o número correspondente:
   - `[1]` para baixar o arquivo completo em **MP4**.
   - `[2]` para extrair apenas o áudio em **MP3**.
4. Aguarde o fim do processo. O arquivo será salvo automaticamente na pasta `Downloads` do seu usuário (ex: `~/Downloads/`).

## 📄 Licença

Sinta-se à vontade para modificar, distribuir e usar este script como base para seus próprios projetos!
README.md
Exibindo README.md.
