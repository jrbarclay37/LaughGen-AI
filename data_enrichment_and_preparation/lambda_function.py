import boto3
import json

# Initialize the DynamoDB and Rekognition clients
dynamodb = boto3.resource('dynamodb')
rekognition = boto3.client('rekognition')

# Reference your DynamoDB table
table = dynamodb.Table('funny-reddit-posts')

def lambda_handler(event, context):
    for record in event['Records']:
        object_key = record['body']  # Example object key: 'reddit/funny/posts/16ok566.jpg'
        bucket_name = 'your-bucket-name'  # Your S3 bucket name

        # Extract submissionId using the helper function
        submissionId = extract_submission_id(object_key)

        # Call Rekognition for Celebrity Recognition
        celebrity_response = rekognition.recognize_celebrities(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
        )
        celebrities = [celeb['Name'] for celeb in celebrity_response['CelebrityFaces']]
        
        # Call Rekognition for Text Detection
        text_response = rekognition.detect_text(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
        )
        detected_texts = [text['DetectedText'] for text in text_response['TextDetections']]

        # Update the DynamoDB item with celebrity and text recognition data
        response = table.update_item(
            Key={'submissionId': submissionId},
            UpdateExpression="SET celebrityRekognition = :celebrities, textRekognition = :texts",
            ExpressionAttributeValues={
                ':celebrities': celebrities,
                ':texts': detected_texts
            },
            ReturnValues="UPDATED_NEW"
        )
        
        print(f"Updated DynamoDB item for submissionId {submissionId}")

def extract_submission_id(object_key):
    # Split the object key to isolate '16ok566.jpg' and then remove the '.jpg'
    filename = object_key.split('/')[-1]
    submission_id = filename.split('.')[0]
    return submission_id
