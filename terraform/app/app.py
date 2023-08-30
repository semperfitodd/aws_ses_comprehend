import os
import json
import boto3
import logging
import email
import datetime
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')

# Retrieve DynamoDB table name from environment variable
table_name = os.environ.get('ENVIRONMENT')
table = dynamodb.Table(table_name)

def extract_email_body(message):
    msg = email.message_from_string(message)

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload()
    else:
        return msg.get_payload()

def generate_unique_id():
    # Combining current datetime with a unique UUID for extra uniqueness
    return f"{datetime.datetime.utcnow().isoformat()}-{uuid.uuid4()}"

def lambda_handler(event, context):
    logger.info("Received event: {}".format(json.dumps(event)))

    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    mail = sns_message['mail']
    source = mail['source']
    subject = mail['commonHeaders']['subject']

    raw_content = sns_message['content']
    content = extract_email_body(raw_content) # Get the plain text content

    key_phrases_response = comprehend.detect_key_phrases(Text=content, LanguageCode='en')
    key_phrases_list = [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]
    key_phrases = '. '.join(key_phrases_list)

    sentiment_response = comprehend.detect_sentiment(Text=content, LanguageCode='en')
    sentiment = sentiment_response['Sentiment']

    uuid = generate_unique_id()

    response = table.put_item(
        Item={
            'uuid': uuid,
            'sender': source,
            'subject': subject,
            'content': content,
            'key_phrases': key_phrases,
            'sentiment': sentiment
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Email key phrases and sentiment extracted and saved successfully!')
    }
