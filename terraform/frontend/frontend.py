import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

# Retrieve DynamoDB table name from environment variable
table_name = os.environ.get('ENVIRONMENT')
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    # 1. Fetch data by sentiments
    sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    sentiment_counts = {}

    for sentiment in sentiments:
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('sentiment').eq(sentiment)
        )
        sentiment_counts[sentiment] = response['Count']

    # 2. Fetch top 10 phrases from each sentiment (This is a basic example and might need refining)
    top_phrases = {}
    for sentiment in sentiments:
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('sentiment').eq(sentiment)
        )
        all_phrases = []
        for item in response['Items']:
            all_phrases.extend(item['key_phrases'].split('. '))
        # Using a simple count, might need more advanced analytics for meaningful phrases
        phrase_count = {phrase: all_phrases.count(phrase) for phrase in set(all_phrases)}
        sorted_phrases = sorted(phrase_count.items(), key=lambda x: x[1], reverse=True)
        top_phrases[sentiment] = [phrase[0] for phrase in sorted_phrases[:10]]

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
        },
        'body': json.dumps({
            'sentimentCounts': sentiment_counts,
            'topPhrases': top_phrases
        })
    }
