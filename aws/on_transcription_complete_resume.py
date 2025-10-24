import json
import boto3
import urllib.parse
import logging
from openai import OpenAI  # pip install openai - LAMBDA LAYER
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

BUCKET_NAME = "amzn-s3-transciption-audios-bucket"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

s3 = boto3.client('s3')
transcribe = boto3.client("transcribe")
openai_client = OpenAI()
openai_client.api_key = OPENAI_API_KEY

#
#    Devido aos custos da OpenAI e de outras aplicações AI Generativas, não foi possível desenvolver esta feature
#

def lambda_handler(event, context):
    sns_message = event["Records"][0]["Sns"]["Message"]
    logger.info(f"📥 Evento recebido: {sns_message}")

    job_data = json.loads(sns_message)
    job_name = job_data["TranscriptionJobName"]
    status = job_data["TranscriptionJobStatus"]

    if status == "FAILED":
        logger.warning(f"Job {job_name} terminou processo com falha")
        return

    uri = get_transcription_uri(job_name)
    transcription_text, video_id = get_transcription_text_from_s3(uri)

    # Gerar resumo com IA
    resume_text = summarize_with_openai(transcription_text)

    save_resume_to_s3(video_id, resume_text)

    return {"message": "Resumo gerado e salvo com sucesso."}


def get_transcription_uri(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]


def get_transcription_text_from_s3(uri):
    parsed = urllib.parse.urlparse(uri)
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")

    logger.info(f"### Lendo transcrição de s3://{bucket}/{key}")

    obj = s3.get_object(Bucket=bucket, Key=key)
    content = json.loads(obj['Body'].read())
    text = content["results"]["transcripts"][0]["transcript"]

    # Extrai video_id da key
    video_id = key.split("/")[0]

    return text, video_id


def summarize_with_openai(transcript_text):
    logger.info("### Enviando texto para OpenAI...")

    prompt = f"""
Você é um assistente que cria resumos concisos. Gere um resumo em português claro e objetivo do conteúdo abaixo:

"{transcript_text[:4000]}"  # limite de tokens
"""

    response = openai_client.responses.create(
        model="gpt-5",
        input=prompt,
    )

    return response.output_text


def save_resume_to_s3(video_id, resumo_text):
    key = f"{video_id}/AI-resume-{video_id}.md"
    logger.info(f"### Salvando resumo em s3://{BUCKET_NAME}/{key}")

    resumo_formatado = f"# Resumo do Vídeo {video_id}\n\n{resumo_text}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=resumo_formatado.encode("utf-8"),
        ContentType="text/markdown"
    )
    logger.info(f"#### Resumo salvo para vídeo {video_id}")
