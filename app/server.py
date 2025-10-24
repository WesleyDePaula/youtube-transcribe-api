import os
from flask import Flask, request, jsonify
from transcription_trigger import start_transcription
from utils import extract_video_id, get_logger
from yt_dlp_client import download
from s3_client import upload_to_s3, get_s3_uri_from_video_id, get_transcription_presigned_URL
from cookies_generator import generate_youtube_cookies

app = Flask(__name__)

logger = get_logger(__name__)


@app.route("/resumeVideoYoutube", methods=["POST"])
def start_resume_from_youtube():
    """
    Não funciona os cookies gerados pelo playwright serem usados na AWS. <br>
    A partir da url de um vídeo do YouTube, realiza o download do áudio, faz upload para S3 e inicia a transcrição com resumo por IA. <br><br>
    ***params: video_url*** URL do vídeo no YouTube
    """
    
    logger.info('### Requisitado resumo de vídeo YouTube')
    
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"error": "Missing video_url"}), 400

    try:
        video_id = extract_video_id(video_url)
        
        logger.info(f'### Cookies no forno...')
        generate_youtube_cookies()
        
        audio_path = download(video_url, video_id)
        
        s3_uri = upload_to_s3(audio_path, video_id)

        start_transcription(video_id, s3_uri)

        return jsonify({
            "message": "Download e transcrição iniciados com sucesso.",
            "video_id": video_id,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route("/resumeVideo", methods=["POST"])
def start_resume_from_video_id():
    """
    A partir do id de um áudio salvo no S3, realiza a transcrição com resumo por IA. <br>
    O áudio deve ser salvo com o seguinte padrão: /<video_id>/youtube-audio-<video_id>.mp3
    <br><br>
    ***params: video_id*** URI do áudio no S3
    """
    
    logger.info('### Requisitado resumo de áudio')
    
    data = request.get_json()
    video_id = data.get("video_id")
    
    start_transcription(video_id, get_s3_uri_from_video_id(video_id))
    
    return jsonify({
            "status": "Processing",
            "video_id": video_id,
        })
    
    
@app.route("/getTranscription", methods=["GET"])
def get_resume_video():
    data = request.get_json()
    video_id = data.get("video_id")
    
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400
    
    uri = get_transcription_presigned_URL(video_id)
    return jsonify({
            "uri": uri,
        })

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080) 
    
