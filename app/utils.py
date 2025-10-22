def extract_video_id(url):
    import re
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def build_transcription_s3_uri(video_id):
    return f"https://s3.amazonaws.com/meu-bucket/transcricoes/{video_id}/transcription.json"

def get_logger(name):
    import logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger