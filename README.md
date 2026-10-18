# Baixador Multimídia em Python

Script em Python para baixar vídeos e playlists do YouTube, com opção de salvar apenas o vídeo (MP4) ou apenas o áudio (MP3). Playlists são organizadas automaticamente em pastas próprias. Compatível com Windows e Linux sem necessidade de ajustes manuais no código.

## Funcionalidades

- Reconhece automaticamente se o link informado é de uma playlist ou de um vídeo individual.
- Download em Lote (`links.txt`): Adicione um arquivo de texto na pasta do projeto contendo um link por linha. O programa reconhece o arquivo automaticamente e processa toda a fila de downloads sequencialmente.
- Playlists são salvas em uma pasta com o nome da playlist, dentro do diretório `Downloads` do usuário.
- Vídeo: baixado em `MP4`, combinando a melhor faixa de vídeo e a melhor faixa de áudio disponíveis quando o FFmpeg está instalado.
- Áudio: extraído e convertido para `MP3` a 192kbps.
- Localiza o FFmpeg automaticamente a partir do `PATH` do sistema — não há caminhos fixos no código.
- Em playlists, itens indisponíveis (privados, removidos, etc.) são pulados automaticamente e listados com o motivo ao final, em vez de interromper todo o download.
- Suporte opcional a cookies do navegador (`--cookies-from-browser` do yt-dlp), para baixar vídeos que exigem login (ex.: restrição de idade).
- Modo contínuo: Após baixar um item ou processar a fila, o script permite continuar baixando links soltos sem precisar reiniciar o programa. Para encerrar, basta pressionar `Ctrl+C`.
- Logs de sessão (`logs/video_downloader.log`): Registra o histórico de todas as execuções em um único arquivo na pasta do projeto (separadas por data, hora e PID), incluindo dados do ambiente (Python, yt-dlp, FFmpeg/Deno), opções escolhidas, links processados, saída do yt-dlp e o traceback completo de eventuais erros.

## Pré-requisitos

- Python 3.10 ou superior (exigido pelas versões atuais do yt-dlp)
- [FFmpeg](https://ffmpeg.org/), necessário para extração de áudio em MP3 e para combinar vídeo e áudio em qualidade máxima
- [Deno](https://deno.com/), runtime JavaScript que o yt-dlp usa para ler o YouTube; já é instalado automaticamente pelo `requirements.txt`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

2. Instale as dependências Python:

   ```bash
   pip install -r requirements.txt
   ```

3. Instale o FFmpeg e garanta que ele esteja no `PATH` do sistema:

   - **Windows:** `winget install ffmpeg` (ou baixe os binários em [ffmpeg.org](https://ffmpeg.org/download.html) e adicione a pasta `bin` às variáveis de ambiente `PATH`).
   - **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`
   - **Linux (Arch):** `sudo pacman -S ffmpeg`
   - **macOS:** `brew install ffmpeg`

   Para confirmar que a instalação foi reconhecida, rode `ffmpeg -version` em um terminal novo. Se o comando funcionar, o script encontra o FFmpeg automaticamente — não é necessário editar nada no código.

   O Deno é instalado junto pelo `requirements.txt` e o script o encontra sozinho, mesmo fora do `PATH`. Se você já tiver o Deno instalado no sistema, ele terá preferência. O log da sessão mostra qual Deno foi usado.

## Como usar

### 1. Preparação
Execute o script no terminal:
```bash
python video_downloader.py
```
Escolha o formato de saída (`1` para MP4 ou `2` para MP3) e informe o navegador para reaproveitar cookies (opcional, para vídeos com restrição).

### 2. Escolha o Modo de Download

#### Modo em Lote (Recomendado para múltiplos arquivos)
Se você tiver vários arquivos para baixar:
1. Crie um arquivo chamado `links.txt` na mesma pasta do script.
2. Cole os links dentro do arquivo, colocando **um link por linha** (pode misturar links de vídeos e playlists).
3. Ao rodar o script, ele detectará o arquivo e perguntará: `"Arquivo links.txt encontrado na pasta! Deseja baixar os links listados nele? (s/n)"`.
4. Digite `s`. O programa vai baixar todos os itens automaticamente. 
5. Ao terminar, ele perguntará se você quer continuar baixando mais coisas manualmente.

#### Modo Manual (Tradicional)
Se não houver um `links.txt` na pasta ou se você digitar `n` na detecção:
1. O script pedirá para você colar a URL diretamente no terminal.
2. O arquivo será salvo na sua pasta `Downloads` (`~/Downloads`).
3. Ao terminar, ele pedirá um novo link. Repita quantas vezes quiser ou pressione `Ctrl+C` para encerrar.

---

**Erros Comuns:**
- Se o FFmpeg não for encontrado, a opção de vídeo baixa uma qualidade combinada menor e a de áudio é bloqueada.
- Aviso `No supported JavaScript runtime could be found`: o Deno não foi encontrado; rode novamente `pip install -r requirements.txt`.
- Se o YouTube parar de funcionar de repente, atualize o yt-dlp: `pip install -U -r requirements.txt`.
- Se algum vídeo de uma playlist ou do seu `links.txt` falhar (privado, removido, etc.), o erro será guardado e listado apenas no final, sem travar o restante da fila.

Para depurar um problema, basta copiar o trecho da sessão desejada. Para limpar, apague o arquivo `logs/video_downloader.log` (a pasta é ignorada pelo Git); ele será recriado na próxima execução.

## Licença

Sinta-se à vontade para modificar, distribuir e usar este script como base para seus próprios projetos.
