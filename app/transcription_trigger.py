import boto3

lambda_client = boto3.client("lambda", region_name='us-west-2')

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
