import json

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = record['body']
        print(f"Received SQS message: {message_body}")
    return {
        'statusCode': 200,
        'body': json.dumps('SQS message processed successfully!')
    }