import yt_dlp # Biblioteca de download de vídeos
import os  # Biblioteca do sistema operacional

# Envio do link do vídeo ou playlist
print("=== Baixador Multimídia do YouTube ===")
link_do_video = input("Cole o link aqui: ")

# Verifica se é uma playlist ou um link solto para definir o local de salvamento
if "list=" in link_do_video:
    # Formato para Playlists: Cria a pasta, mas usa APENAS o título original da música
    caminho_salvar = os.path.expanduser('~/Downloads/%(playlist)s/%(title)s.%(ext)s')
    print("\n📦 Playlist detectada! As músicas serão salvas com os nomes originais em uma pasta própria.")
else:
    # Formato para Arquivos Soltos: Salva direto na pasta padrão de Downloads
    caminho_salvar = os.path.expanduser('~/Downloads/%(title)s.%(ext)s')
    print("\n🎵 Arquivo individual detectado!")

# Seleção do formato de download
print("\nO que você deseja baixar?")
print("[1] Apenas o Vídeo (MP4)")
print("[2] Apenas o Áudio (MP3)")
escolha = input("Digite 1 ou 2: ")

# Variável de configurações vazia para receber as configurações do formato escolhido
configuracoes = None

# Definição das configurações para o formato .mp4
if escolha == "1":
    configuracoes = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': caminho_salvar 
    }
    print("\nPreparando o download do Vídeo...")

# Definição das configurações para o formato .mp3
elif escolha == "2":
    configuracoes = {
        'format': 'bestaudio/best',
        'outtmpl': caminho_salvar,
        # Caminho do FFmpeg mantido
        'ffmpeg_location': r'C:\Users\ryanb\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    print("\nPreparando o download do Áudio...")

# Opção para caso o usuário selecione uma opção fora das disponíveis
else:
    print("\nOpção inválida! Encerrando o programa...")

# Execução do download
if configuracoes is not None:
    try:
        with yt_dlp.YoutubeDL(configuracoes) as motor_de_download:
            motor_de_download.download([link_do_video])
        print("\n✅ Download concluído com sucesso! Verifique a sua pasta de Downloads.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro durante o download: {e}")