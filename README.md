# Baixador Multimídia em Phyton

Script em Python para baixar vídeos e playlists do YouTube, com opção de salvar apenas o vídeo (MP4) ou apenas o áudio (MP3). Playlists são organizadas automaticamente em pastas próprias. Compatível com Windows e Linux sem necessidade de ajustes manuais no código.

## Funcionalidades

- Reconhece automaticamente se o link informado é de uma playlist ou de um vídeo individual.
- Playlists são salvas em uma pasta com o nome da playlist, dentro do diretório `Downloads` do usuário.
- Vídeo: baixado em `MP4`, combinando a melhor faixa de vídeo e a melhor faixa de áudio disponíveis quando o FFmpeg está instalado.
- Áudio: extraído e convertido para `MP3` a 192kbps.
- Localiza o FFmpeg automaticamente a partir do `PATH` do sistema — não há caminhos fixos no código.
- Em playlists, itens indisponíveis (privados, removidos, etc.) são pulados automaticamente e listados com o motivo ao final, em vez de interromper todo o download.
- Suporte opcional a cookies do navegador (`--cookies-from-browser` do yt-dlp), para baixar vídeos que exigem login (ex.: restrição de idade).
- Modo contínuo: as opções (formato e cookies) são definidas apenas uma vez. Depois disso, o script fica pedindo o próximo link automaticamente após cada download, sem precisar reiniciar o programa — ideal para baixar várias playlists ou episódios de uma série em sequência. Para encerrar, basta pressionar `Ctrl+C`.

## Pré-requisitos

- Python 3.8 ou superior
- [FFmpeg](https://ffmpeg.org/), necessário para extração de áudio em MP3 e para combinar vídeo e áudio em qualidade máxima

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

## Como usar

1. Execute o script:

   ```bash
   python video_downloader.py
   ```

2. Escolha o formato de saída:
   - `1` para baixar o vídeo completo em MP4.
   - `2` para extrair apenas o áudio em MP3.
3. Informe o navegador de onde reaproveitar os cookies de login (`chrome`, `firefox`, `edge`, `brave`, etc.), ou deixe em branco para pular. Isso só é necessário para vídeos que exigem autenticação (ex.: restrição de idade). **Feche o navegador escolhido antes de continuar**, já que o arquivo de cookies fica bloqueado enquanto ele está aberto.
4. Cole a URL do vídeo ou da playlist quando solicitado. O arquivo será salvo na pasta `Downloads` do usuário (`~/Downloads`).
5. Ao terminar o download, o script pede automaticamente o próximo link — repita o passo 4 quantas vezes quiser, sem precisar reiniciar o programa. Quando não houver mais nada para baixar, pressione `Ctrl+C` para encerrar.

Se o FFmpeg não for encontrado, o script informa isso na tela: a opção de vídeo passa a usar uma qualidade combinada já pronta (sem juntar faixas separadas), e a opção de áudio é bloqueada, já que a conversão para MP3 depende do FFmpeg.

Ao final do download de uma playlist, se algum item não puder ser baixado (vídeo privado, removido, exige login sem cookies configurados, etc.), o script exibe a lista completa dos itens que falharam junto com o motivo de cada falha — o restante da playlist é baixado normalmente, e o programa segue pronto para receber o próximo link.

## Licença

Sinta-se à vontade para modificar, distribuir e usar este script como base para seus próprios projetos.
