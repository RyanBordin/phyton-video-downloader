import logging
import os
import platform
import shutil
import sys
from datetime import datetime
from urllib.parse import parse_qs, urlparse

import yt_dlp  # Biblioteca de download de videos

DOWNLOADS_DIR = os.path.expanduser('~/Downloads')
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
CAMINHO_LOG = os.path.join(LOGS_DIR, 'video_downloader.log')

log = logging.getLogger('video_downloader')


class HandlerQueGravaNaHora(logging.FileHandler):
    """Grava cada linha no disco imediatamente, para o log nao se perder se o
    terminal for fechado no meio da sessao."""

    def emit(self, record):
        super().emit(record)
        os.fsync(self.stream.fileno())


def localizar_deno():
    """Procura o Deno (runtime JavaScript usado pelo yt-dlp no YouTube): primeiro no
    PATH, depois no pacote 'deno' instalado pelo requirements.txt, que fica na pasta
    Scripts/bin da .venv e nao esta no PATH quando a .venv nao foi ativada."""
    caminho = shutil.which('deno')
    if caminho:
        return caminho
    try:
        import deno
        return deno.find_deno_bin()
    except (ImportError, FileNotFoundError):
        return None


def localizar_ffmpeg():
    """Procura o FFmpeg: primeiro no PATH (instalacao do sistema, que costuma vir com o
    ffprobe), depois no binario que o pacote 'imageio-ffmpeg' do requirements.txt traz."""
    caminho = shutil.which('ffmpeg')
    if caminho:
        return caminho
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except (ImportError, RuntimeError):
        return None


def configurar_log() -> str:
    """Abre o arquivo de log unico do projeto ('logs/video_downloader.log').
    Cada sessao e acrescentada ao final, mantendo o historico das anteriores."""
    os.makedirs(LOGS_DIR, exist_ok=True)

    handler = HandlerQueGravaNaHora(CAMINHO_LOG, mode='a', encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    id_sessao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.info('=' * 70)
    log.info('=== Inicio da sessao %s (PID %d) ===', id_sessao, os.getpid())
    log.info('Executavel: %s', sys.executable)
    log.info('Sistema: %s | Python %s', platform.platform(), sys.version.split()[0])
    log.info('yt-dlp: %s', yt_dlp.version.__version__)
    log.info('FFmpeg: %s', localizar_ffmpeg() or 'nao encontrado')
    log.info('Deno: %s', localizar_deno() or 'nao encontrado')
    log.info('Pasta de downloads: %s', DOWNLOADS_DIR)
    return CAMINHO_LOG


def deve_baixar_playlist(link_do_video: str) -> bool:
    """Decide se o link deve ser tratado como playlist ou apenas como o video indicado.

    - Link sem 'list=': video individual.
    - Link de playlist pura (sem 'v='): playlist inteira.
    - Link com 'v=' e 'list=RD...': e um Mix gerado automaticamente pelo YouTube
      (centenas de itens), entao baixa so o video escolhido.
    - Link com 'v=' e uma playlist comum: pergunta ao usuario.
    """
    parametros = parse_qs(urlparse(link_do_video).query)
    id_playlist = parametros.get('list', [''])[0]
    id_video = parametros.get('v', [''])[0]

    if not id_playlist:
        return False
    if not id_video:
        return True
    if id_playlist.startswith('RD'):
        print('\nLink de Mix do YouTube detectado! Baixando apenas o video escolhido.')
        log.info('Mix detectado (list=%s): baixando apenas o video %s', id_playlist, id_video)
        return False

    resposta = input('\nEste link aponta para um video dentro de uma playlist. '
                     'Baixar a playlist inteira? (s/n): ').strip().lower()
    log.info('Video %s dentro da playlist %s. Baixar playlist inteira? %r',
             id_video, id_playlist, resposta)
    return resposta == 's'


def montar_template_de_saida(baixar_playlist: bool) -> str:
    """Define onde o arquivo sera salvo, com base no tipo de link (playlist ou video solto)."""
    if baixar_playlist:
        print('\nPlaylist detectada! As musicas serao salvas com os nomes originais em uma pasta propria.')
        return os.path.join(DOWNLOADS_DIR, '%(playlist)s', '%(title)s.%(ext)s')

    print('\nArquivo individual detectado!')
    return os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s')


def montar_configuracoes(escolha: str, caminho_salvar: str):
    """Monta as configuracoes do yt-dlp de acordo com o formato escolhido."""
    ffmpeg_path = localizar_ffmpeg()

    if escolha == '1':
        configuracoes = {'outtmpl': caminho_salvar, 'ignoreerrors': True}
        if ffmpeg_path:
            # Com FFmpeg disponivel, baixa o melhor video e o melhor audio
            # separadamente e junta em um unico MP4.
            configuracoes['ffmpeg_location'] = ffmpeg_path
            configuracoes['format'] = 'bestvideo+bestaudio/best'
            configuracoes['merge_output_format'] = 'mp4'
        else:
            # Sem FFmpeg nao e possivel juntar faixas separadas, entao usa
            # um MP4 que ja venha com video e audio combinados.
            configuracoes['format'] = 'best[ext=mp4]/best'
            print('\nAviso: FFmpeg nao encontrado no PATH. Baixando na melhor qualidade '
                  'disponivel sem juntar faixas separadas de video e audio.')
            log.warning('FFmpeg nao encontrado: video sera baixado sem juntar faixas')
        print('\nPreparando o download do Video...')
        return configuracoes

    if escolha == '2':
        if not ffmpeg_path:
            print('\nErro: a extracao de audio em MP3 requer o FFmpeg instalado e '
                  'disponivel no PATH do sistema.')
            log.error('FFmpeg nao encontrado: extracao de MP3 impossivel')
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
    log.error('Opcao de formato invalida: %r', escolha)
    return None


def obter_cookies_do_navegador():
    """Pergunta de qual navegador reaproveitar os cookies de login (para videos
    que exigem autenticacao). Deixar em branco pula essa etapa."""
    navegador = input(
        '\nNavegador para usar cookies de login (chrome, firefox, edge, brave...), '
        'ou deixe em branco para pular: '
    ).strip().lower()
    return (navegador,) if navegador else None


def eh_linha_de_progresso(msg: str) -> bool:
    """Linhas de progresso ('[download]  45.3% of ... ETA ...') sao atualizadas
    varias vezes por segundo; ficam so no terminal para nao inflar o log."""
    return msg.startswith('[download]') and 'ETA' in msg


class ColetorDeFalhas:
    """Logger customizado do yt-dlp: deixa a saida normal passar, grava tudo no
    arquivo de log e guarda os erros (que ja vem com o motivo) para listar no
    final, sem interromper a playlist."""

    def __init__(self):
        self.falhas = []

    def debug(self, msg):
        if msg.startswith('[debug] '):
            log.debug('yt-dlp: %s', msg)
            return
        print(msg)
        if not eh_linha_de_progresso(msg):
            log.info('yt-dlp: %s', msg)

    def warning(self, msg):
        print(f'AVISO: {msg}')
        log.warning('yt-dlp: %s', msg)

    def error(self, msg):
        print(f'ERRO: {msg}')
        log.error('yt-dlp: %s', msg)
        self.falhas.append(msg)


def baixar_link(link_do_video: str, escolha: str, cookies_navegador) -> None:
    """Baixa um unico link (video ou playlist) com as opcoes ja definidas."""
    log.info('--- Novo link: %s', link_do_video)
    baixar_playlist = deve_baixar_playlist(link_do_video)
    caminho_salvar = montar_template_de_saida(baixar_playlist)
    configuracoes = montar_configuracoes(escolha, caminho_salvar)
    if configuracoes is None:
        return

    # Sem isso o yt-dlp baixa a playlist inteira quando o link tem 'v=' e 'list='.
    configuracoes['noplaylist'] = not baixar_playlist

    if cookies_navegador:
        configuracoes['cookiesfrombrowser'] = cookies_navegador

    caminho_deno = localizar_deno()
    if caminho_deno:
        configuracoes['js_runtimes'] = {'deno': {'path': caminho_deno}}

    log.info('Configuracoes do yt-dlp: %s', configuracoes)

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
            log.warning('Link concluido com %d falha(s)', len(coletor_de_falhas.falhas))
        else:
            print('\nDownload concluido com sucesso! Verifique a sua pasta de Downloads.')
            log.info('Link concluido com sucesso')
    except Exception as e:
        print(f'\nOcorreu um erro durante o download: {e}')
        log.exception('Erro inesperado ao baixar %s', link_do_video)


def main():
    print('=== Baixador Multimidia do YouTube ===')

    print('\nO que voce deseja baixar?')
    print('[1] Apenas o Video (MP4)')
    print('[2] Apenas o Audio (MP3)')
    escolha = input('Digite 1 ou 2: ').strip()
    log.info('Formato escolhido: %r', escolha)

    if escolha not in ('1', '2'):
        print('\nOpcao invalida! Encerrando o programa...')
        log.error('Opcao de formato invalida: %r', escolha)
        sys.exit(1)

    if escolha == '2' and not localizar_ffmpeg():
        print('\nErro: a extracao de audio em MP3 requer o FFmpeg instalado e '
              'disponivel no PATH do sistema.')
        log.error('FFmpeg nao encontrado: extracao de MP3 impossivel')
        sys.exit(1)

    cookies_navegador = obter_cookies_do_navegador()
    log.info('Cookies do navegador: %s', cookies_navegador[0] if cookies_navegador else 'nao')
    if cookies_navegador:
        print(f'\nAviso: feche o navegador "{cookies_navegador[0]}" antes de continuar, '
              'senao o arquivo de cookies pode estar bloqueado.')

    # --- LÓGICA DO ARQUIVO .TXT ---
    caminho_txt = 'links.txt'
    modo_manual = True

    if os.path.exists(caminho_txt):
        usar_txt = input(f'\nArquivo {caminho_txt} encontrado na pasta! Deseja baixar os links listados nele? (s/n): ').strip().lower()
        log.info('%s encontrado. Usar? %r', caminho_txt, usar_txt)
        if usar_txt == 's':
            modo_manual = False
            try:
                with open(caminho_txt, 'r', encoding='utf-8') as f:
                    links_arquivo = [linha.strip() for linha in f if linha.strip()]

                if not links_arquivo:
                    print(f'\nO arquivo {caminho_txt} esta vazio. Iniciando o modo manual...')
                    log.warning('%s esta vazio', caminho_txt)
                    modo_manual = True
                else:
                    print(f'\nIniciando o download de {len(links_arquivo)} link(s) a partir de {caminho_txt}...')
                    log.info('Modo em lote: %d link(s) em %s', len(links_arquivo), caminho_txt)
                    for i, link_do_video in enumerate(links_arquivo, 1):
                        print(f'\n--- Processando link {i}/{len(links_arquivo)} do arquivo ---')
                        log.info('Lote: link %d/%d', i, len(links_arquivo))
                        baixar_link(link_do_video, escolha, cookies_navegador)

                    print(f'\nTodos os links do {caminho_txt} foram processados!')
                    log.info('Modo em lote concluido')

                    continuar = input('\nDeseja continuar baixando outros links manualmente? (s/n): ').strip().lower()
                    if continuar == 's':
                        modo_manual = True
                    else:
                        print('\nEncerrando o programa. Ate mais!')
                        sys.exit(0)
            except Exception as e:
                print(f'\nErro ao ler o arquivo {caminho_txt}: {e}')
                print('Iniciando o modo manual por precaução...')
                log.exception('Erro ao processar %s', caminho_txt)
                modo_manual = True

    # --- MODO MANUAL (PADRÃO) ---
    if modo_manual:
        print('\nTudo pronto! Cole um link por vez para baixar (video ou playlist).')
        print('Pressione Ctrl+C a qualquer momento para encerrar o programa.')
        log.info('Modo manual iniciado')

        try:
            while True:
                link_do_video = input('\nCole o link aqui: ').strip()
                if not link_do_video:
                    print('Nenhum link informado. Tente novamente.')
                    continue

                baixar_link(link_do_video, escolha, cookies_navegador)
        except KeyboardInterrupt:
            print('\n\nEncerrando o programa. Ate mais!')
            sys.exit(0)


if __name__ == '__main__':
    caminho_log = configurar_log()
    print(f'Log: {caminho_log}\n')
    try:
        main()
    except KeyboardInterrupt:
        log.info('Sessao interrompida pelo usuario (Ctrl+C)')
        print('\n\nEncerrando o programa. Ate mais!')
    except Exception:
        log.exception('Erro nao tratado encerrou o programa')
        raise
    finally:
        log.info('=== Fim da sessao ===')
