import boto3
import whisper
import boto3

model = whisper.load_model("tiny")
s3_client = boto3.client('s3')

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
    
    result = model.transcribe(f'/tmp/youtube-audio-{video_id}.mp3')
    
    print('### Transcrição concluída. Salvando resultado no S3...')
    s3_client.put_object(
        Bucket='amzn-s3-transciption-audios-bucket',
        Key=f"{video_id}/transcription-{video_id}.txt",
        Body=result["text"].encode('utf-8')
    )
    
    # Contruindo a URI para download do arquivo salvo com boto3
    s3_uri = f"s3://amzn-s3-transciption-audios-bucket/{video_id}/transcription-{video_id}.txt"

    return {
        "message": "Transcription completed and saved to S3",
        "video_id": video_id,
        "s3_uri": s3_uri
    }
    
    # chamada transcribe -- NÃO FUNCIONA, TA DE ENFEITE PARA CASO EU PRECISE
    # transcribe = boto3.client("transcribe", region_name="us-east-2")
    # job_name = f"transcribe-{video_id}"
    # transcribe.start_transcription_job(
    #     TranscriptionJobName=job_name,
    #     IdentifyLanguage=True,
    #     MediaFormat="mp3",
    #     Media={"MediaFileUri": s3_uri},
    #     OutputBucketName="amzn-s3-transciption-audios-bucket",
    #     OutputKey=f"{video_id}/"
    # )
    # return {"message": "Transcription started", "job_name": job_name}



