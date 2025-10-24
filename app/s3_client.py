import os
import boto3
from utils import get_logger

s3 = boto3.client('s3')
BUCKET_NAME = 'amzn-s3-transciption-audios-bucket'

logger = get_logger(__name__)


def upload_to_s3(filepath, video_id):
    '''
    Realiza o upload do arquivo de áudio para o bucket S3.
    '''
    key_name = f"{video_id}/{os.path.basename(filepath)}"
    
    logger.info(f"### Realizando upload do áudio {filepath} ao S3://{BUCKET_NAME}/{key_name}")
    with open(filepath, 'rb') as f:
        s3.upload_fileobj(f, BUCKET_NAME, key_name)
    logger.info("### Upload concluído.")
    return f"s3://{BUCKET_NAME}/{key_name}"


def get_resume_presigned_URL(video_id):
    '''
    Gerar uma URL para download do arquivo de resumo da transcrição sem precisar de autenticação na AWS.
    '''
    key_name = f"{video_id}/transcription_resume.txt"
    
    logger.info(f"### Gerando URL pré-assinada para o arquivo de resumo: S3://{BUCKET_NAME}/{key_name}")
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key_name},
        ExpiresIn=3600
    )
    return presigned_url

def get_transcription_presigned_URL(video_id):
    '''
    Gerar uma URL para download do arquivo da transcrição sem precisar de autenticação na AWS.
    '''
    key_name = f"{video_id}/transcription-{video_id}.txt"
    
    logger.info(f"### Gerando URL pré-assinada para o arquivo: S3://{BUCKET_NAME}/{key_name}")
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key_name},
        ExpiresIn=3600
    )
    return presigned_url

def get_s3_uri_from_video_id(video_id):
    '''
    Retorna a URI S3 do áudio baseado no video_id.
    '''
    key_name = f"{video_id}/youtube-audio-{video_id}.mp3"
    return f"s3://{BUCKET_NAME}/{key_name}"