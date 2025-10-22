import os
import boto3
import logging

s3 = boto3.client('s3')
BUCKET_NAME = 'amzn-s3-transciption-audios-bucket'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


'''
    Realiza o upload do arquivo de áudio para o bucket S3.
'''
def upload_to_s3(filepath, video_id):
    key_name = f"{video_id}/{os.path.basename(filepath)}"
    
    logger.info(f"### Realizando upload do áudio {filepath} ao S3://{BUCKET_NAME}/{key_name}")
    with open(filepath, 'rb') as f:
        s3.upload_fileobj(f, BUCKET_NAME, key_name)
    logger.info("### Upload concluído.")
    return f"s3://{BUCKET_NAME}/{key_name}"


'''
    Gerar uma URL para download do arquivo de resumo da transcrição sem precisar de autenticação na AWS.
'''
def get_resume_presigned_URL(video_id):
    key_name = f"{video_id}/transcription_resume.txt"
    
    logger.info(f"### Gerando URL pré-assinada para o arquivo de resumo: S3://{BUCKET_NAME}/{key_name}")
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key_name},
        ExpiresIn=3600
    )
    return presigned_url