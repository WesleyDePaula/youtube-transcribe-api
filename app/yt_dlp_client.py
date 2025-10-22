import yt_dlp
import logging
from utils import extract_video_id

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO: Verificar se arquivo de áudio será deletado da /tmp/ no final do upload ao S3
def download_from_url(video_url: str, video_id: str):
    filename = f"/tmp/youtube-audio-{video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'cookiefile': '/app/cookies.txt', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    logger.info(f"### Download concluído: {filename}.mp3")
    return filename + ".mp3"

def download(video_url, video_id):
    logger.info(f"### Iniciando download e conversão para áudio do vídeo: {video_url}")
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    return download_from_url(video_url, video_id) 
    
