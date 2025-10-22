def extract_video_id(url):
    import re
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def build_transcription_s3_uri(video_id):
    return f"https://s3.amazonaws.com/meu-bucket/transcricoes/{video_id}/transcription.json"
