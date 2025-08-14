#!/usr/bin/env python3
"""
YouTube Downloader - Ferramenta para baixar vídeos do YouTube
"""
import os
import sys
from urllib.parse import urlparse

from pytube import YouTube, request
from pytube.exceptions import PytubeError

# Configuração de cores para o terminal (ANSI escape codes)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Constantes
VIDEOS_DIR = os.path.join("src", "videos")
SUPPORTED_QUALITIES = ["highest", "lowest", "audio"]

# Patch para evitar HTTP Error 400
request.default_range_size = 1048576  # 1MB chunks

def setup_environment():
    """Cria a estrutura de diretórios necessária"""
    os.makedirs(VIDEOS_DIR, exist_ok=True)

def display_banner():
    """Exibe o banner estilizado do programa"""
    banner = f"""
{Colors.BOLD}{Colors.BLUE}
####################################
#                                  #
#       YouTube Downloader         #
#                                  #
####################################
{Colors.END}
"""
    print(banner)

def is_valid_url(url: str) -> bool:
    """Valida se a URL é do YouTube"""
    try:
        result = urlparse(url)
        return all([
            result.scheme in ("http", "https"),
            "youtube.com" in result.netloc or "youtu.be" in result.netloc
        ])
    except:
        return False

def get_user_input():
    """Obtém a URL e qualidade desejada do usuário"""
    print(f"{Colors.YELLOW}→ Qualidades disponíveis: {', '.join(SUPPORTED_QUALITIES)}{Colors.END}")
    url = input(f"{Colors.BOLD}🔗 Cole a URL do vídeo: {Colors.END}").strip()
    quality = input(f"{Colors.BOLD}📊 Qualidade desejada [{SUPPORTED_QUALITIES[0]}]: {Colors.END}").strip() or SUPPORTED_QUALITIES[0]
    return url, quality

def download_video(url: str, quality: str = "highest"):
    """
    Baixa o vídeo do YouTube com a qualidade especificada
    Retorna o caminho do arquivo baixado ou None em caso de erro
    """
    if not is_valid_url(url):
        print(f"{Colors.RED}❌ URL inválida!{Colors.END}")
        return None

    try:
        yt = YouTube(url)
        stream = None
        if quality == "highest":
            stream = yt.streams.get_highest_resolution()
        elif quality == "lowest":
            stream = yt.streams.get_lowest_resolution()
        elif quality == "audio":
            stream = yt.streams.filter(only_audio=True).first()

        if not stream:
            print(f"{Colors.RED}❌ Nenhum stream disponível para a qualidade selecionada.{Colors.END}")
            return None

        output_path = stream.download(output_path=VIDEOS_DIR)
        return output_path

    except PytubeError as e:
        print(f"{Colors.RED}❌ Erro no YouTube: {e}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Falha ao baixar o vídeo: {e}{Colors.END}")

    return None

def main():
    """Função principal do programa"""
    setup_environment()
    display_banner()
    
    try:
        url, quality = get_user_input()

        if quality.lower() not in SUPPORTED_QUALITIES:
            print(f"{Colors.YELLOW}⚠️  Qualidade inválida. Usando 'highest' como padrão.{Colors.END}")
            quality = "highest"
        
        print(f"{Colors.BLUE}⏳ Processando...{Colors.END}")
        filepath = download_video(url, quality.lower())
        
        if filepath:
            filename = os.path.basename(filepath)
            print(f"{Colors.GREEN}✅ Download concluído!{Colors.END}")
            print(f"{Colors.BOLD}📁 Arquivo salvo em: {os.path.abspath(filepath)}{Colors.END}")
            print(f"{Colors.GREEN}Tamanho: {os.path.getsize(filepath) / (1024*1024):.2f} MB{Colors.END}")
        else:
            print(f"{Colors.RED}❌ Falha ao baixar o vídeo.{Colors.END}")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Operação cancelada pelo usuário.{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
