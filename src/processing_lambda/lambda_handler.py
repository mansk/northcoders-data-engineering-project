import logging
import boto3

def lambda_handler(event, context):
    print(event['Records'])
    print("Hello")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.error("This is an ERROR message")

    s3_client = boto3.client('s3')

    destination_bucket = 'de-watershed-processed-bucket'

    folder_name = 'folder-name'
    file_name = 'example-file.txt'

    file_content = "This is the content of the file."

    destination_object_key = f'{folder_name}/{file_name}'

    s3_client.put_object(
        Bucket=destination_bucket,
        Key=destination_object_key,
        Body=file_content.encode('utf-8')  
    )