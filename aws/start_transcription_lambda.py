import time
import boto3
import requests

whisper_url = "https://api.whisper-api.com/"
s3_client = boto3.client('s3')


headers = {
    "X-API-Key": 'f3ZSSRUgDA1ylbI5CoBqy1EdpS1t_6vQMt_NjsEK75A'
}

def lambda_handler(event, context):
    video_id = event["video_id"]
    s3_uri = event["s3_uri"]

    print('### Baixando audio do S3 ->', s3_uri)
    s3_client.download_file(
        Bucket='amzn-s3-transciption-audios-bucket',
        Key=f"{video_id}/youtube-audio-{video_id}.mp3",
        Filename=f"/tmp/youtube-audio-{video_id}.mp3"
    )

    print('### Iniciando transcrição... ')
    
    
    with open(f'/tmp/youtube-audio-{video_id}.mp3', "rb") as f:
        files = {
            "file": (f'/tmp/youtube-audio-{video_id}.mp3', f, "audio/mpeg")  
        }
        resp = requests.post(f'{whisper_url}/transcribe', headers=headers, files=files, timeout=600).json()
        
    task_id = resp["task_id"]
    processing = True
    while processing:
        result = requests.get(f"{whisper_url}/status/{task_id}", headers=headers, timeout=600).json()
        if result['status'] == 'completed':
            processing = False
        else:
            print('### Transcrição em andamento... Aguardando 10 segundos para nova verificação.')
            time.sleep(10)
    
    print('### Transcrição concluída. Salvando resultado no S3...')
    s3_client.put_object(
        Bucket='amzn-s3-transciption-audios-bucket',
        Key=f"{video_id}/transcription-{video_id}.txt",
        Body=result["result"].encode('utf-8')
    )
    
    # Contruindo a URI para download do arquivo salvo com boto3
    s3_uri = f"s3://amzn-s3-transciption-audios-bucket/{video_id}/transcription-{video_id}.txt"

    print('### Fim')
    return {
        "message": "Transcription completed and saved to S3",
        "video_id": video_id,
        "s3_uri": s3_uri
    }
    