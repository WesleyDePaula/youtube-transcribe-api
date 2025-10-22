from flask import Flask, request, jsonify
from transcription_trigger import start_transcription
from utils import extract_video_id, build_transcription_s3_uri
from yt_dlp_client import download
from aws.s3_client import upload_to_s3

app = Flask(__name__)

'''
    TODO: Documentar endpoints
'''
@app.route("/resumeVideo", methods=["POST"])
def start_resume_video():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"error": "Missing video_url"}), 400

    try:
        video_id = extract_video_id(video_url)
        audio_path = download(video_url, video_id)
        
        s3_uri = upload_to_s3(audio_path, video_id)

        start_transcription(video_id, s3_uri)

        transcription_uri = build_transcription_s3_uri(video_id)

        return jsonify({
            "message": "Download e transcrição iniciados com sucesso.",
            "video_id": video_id,
            "transcription_uri": transcription_uri
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/getResume", methods=["GET"])
def get_resume_video():
    data = request.get_json()
    video_id = data.get("video_id")
    
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400
    
    
    
