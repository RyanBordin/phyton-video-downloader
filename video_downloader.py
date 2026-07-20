import os
import shutil
import sys

import yt_dlp  # Biblioteca de download de videos

DOWNLOADS_DIR = os.path.expanduser('~/Downloads')


def montar_template_de_saida(link_do_video: str) -> str:
    """Define onde o arquivo sera salvo, com base no tipo de link (playlist ou video solto)."""
    if 'list=' in link_do_video:
        print('\nPlaylist detectada! As musicas serao salvas com os nomes originais em uma pasta propria.')
        return os.path.join(DOWNLOADS_DIR, '%(playlist)s', '%(title)s.%(ext)s')

    print('\nArquivo individual detectado!')
    return os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s')


def montar_configuracoes(escolha: str, caminho_salvar: str):
    """Monta as configuracoes do yt-dlp de acordo com o formato escolhido."""
    ffmpeg_path = shutil.which('ffmpeg')

    if escolha == '1':
        configuracoes = {'outtmpl': caminho_salvar, 'ignoreerrors': True}
        if ffmpeg_path:
            # Com FFmpeg disponivel, baixa o melhor video e o melhor audio
            # separadamente e junta em um unico MP4.
            configuracoes['format'] = 'bestvideo+bestaudio/best'
            configuracoes['merge_output_format'] = 'mp4'
        else:
            # Sem FFmpeg nao e possivel juntar faixas separadas, entao usa
            # um MP4 que ja venha com video e audio combinados.
            configuracoes['format'] = 'best[ext=mp4]/best'
            print('\nAviso: FFmpeg nao encontrado no PATH. Baixando na melhor qualidade '
                  'disponivel sem juntar faixas separadas de video e audio.')
        print('\nPreparando o download do Video...')
        return configuracoes

    if escolha == '2':
        if not ffmpeg_path:
            print('\nErro: a extracao de audio em MP3 requer o FFmpeg instalado e '
                  'disponivel no PATH do sistema.')
            return None

        print('\nPreparando o download do Audio...')
        return {
            'format': 'bestaudio/best',
            'outtmpl': caminho_salvar,
            'ffmpeg_location': ffmpeg_path,
            'ignoreerrors': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    print('\nOpcao invalida! Encerrando o programa...')
    return None


def obter_cookies_do_navegador():
    """Pergunta de qual navegador reaproveitar os cookies de login (para videos
    que exigem autenticacao). Deixar em branco pula essa etapa."""
    navegador = input(
        '\nNavegador para usar cookies de login (chrome, firefox, edge, brave...), '
        'ou deixe em branco para pular: '
    ).strip().lower()
    return (navegador,) if navegador else None


class ColetorDeFalhas:
    """Logger customizado do yt-dlp: deixa a saida normal passar e guarda os erros
    (que ja vem com o motivo) para listar no final, sem interromper a playlist."""

    def __init__(self):
        self.falhas = []

    def debug(self, msg):
        if msg.startswith('[debug] '):
            return
        print(msg)

    def warning(self, msg):
        print(f'AVISO: {msg}')

    def error(self, msg):
        print(f'ERRO: {msg}')
        self.falhas.append(msg)


def main():
    print('=== Baixador Multimidia do YouTube ===')
    link_do_video = input('Cole o link aqui: ').strip()

    if not link_do_video:
        print('\nNenhum link informado. Encerrando o programa...')
        sys.exit(1)

    caminho_salvar = montar_template_de_saida(link_do_video)

    print('\nO que voce deseja baixar?')
    print('[1] Apenas o Video (MP4)')
    print('[2] Apenas o Audio (MP3)')
    escolha = input('Digite 1 ou 2: ').strip()

    configuracoes = montar_configuracoes(escolha, caminho_salvar)
    if configuracoes is None:
        sys.exit(1)

    cookies_navegador = obter_cookies_do_navegador()
    if cookies_navegador:
        configuracoes['cookiesfrombrowser'] = cookies_navegador
        print(f'\nAviso: feche o navegador "{cookies_navegador[0]}" antes de continuar, '
              'senao o arquivo de cookies pode estar bloqueado.')

    coletor_de_falhas = ColetorDeFalhas()
    configuracoes['logger'] = coletor_de_falhas

    try:
        with yt_dlp.YoutubeDL(configuracoes) as motor_de_download:
            motor_de_download.download([link_do_video])

        if coletor_de_falhas.falhas:
            print(f'\nDownload concluido, mas {len(coletor_de_falhas.falhas)} '
                  'item(ns) nao puderam ser baixados:')
            for falha in coletor_de_falhas.falhas:
                print(f'  - {falha}')
        else:
            print('\nDownload concluido com sucesso! Verifique a sua pasta de Downloads.')
    except KeyboardInterrupt:
        print('\nDownload cancelado pelo usuario.')
        sys.exit(1)
    except Exception as e:
        print(f'\nOcorreu um erro durante o download: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
