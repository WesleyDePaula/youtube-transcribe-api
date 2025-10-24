import boto3
import json
from utils import get_logger 

lambda_client = boto3.client("lambda", region_name='us-east-2')
logger = get_logger(__name__)

def start_transcription(video_id, s3_uri):
    payload = {
        "video_id": video_id,
        "s3_uri": s3_uri
    }

    lambda_client.invoke(
        FunctionName="start-transcription-lambda",
        InvocationType="Event",
        Payload=json.dumps(payload)
    )
    
