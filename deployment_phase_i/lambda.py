import os
import io
import json
import boto3
import praw
from botocore.exceptions import ClientError
from urllib.request import urlretrieve


def lambda_handler(event, context):

    try:
    
        bucket_name = 'sagemaker-us-east-1-513033806411'

        # Initialize Reddit Client
        reddit = initialize_reddit_client()

        # Extract post URL from the Lambda event
        post_url = event["post_url"]

        # Extracting the post ID from the URL
        post_id = post_url.split('/')[-3]

        # Use PRAW to get the submission object
        submission = reddit.submission(id=post_id)

        # Initialize response dictionary
        response = {
            "id": submission.id,
            "title": submission.title,
            "body": submission.selftext
            "url": submission.url
        }

        prompt = initialize_prompt(response)

        # If there is an image, process it
        if image_url.endswith(('.jpg', '.png')):

            # Download the image to a temporary location
            image_path = download_image(submission.id, submission.url)

            # Upload the image to S3
            object_key = upload_image_to_s3(bucket_name, image_path)

            # Generate an image caption using the BLIP model
            image_caption = generate_caption_from_s3(bucket_name, object_key, endpoint_name)

            celebrities, detected_texts = get_celebrity_text(bucket_name, object_key)

        else:

            image_caption, celebrities, detected_texts = ('','','')

        # format image context
        image_context = format_image_context(image_caption, celebrities, detected_texts)

        #finalize prompt
        final_prompt = finalize_prompt(base_prompt, image_context)

        # Get a response from the Llama2 model using the post title and image caption
        llama_response = get_llama_response(endpoint_name, text_input)

        # Return the response
        return {
            'statusCode': 200,
            'body': json.dumps(llama_response)
        }

    except Exception as e:
        print(str(e))
        return "Error generating comment"


def get_secret():
    """Get secret from AWS Secrets Manager"""

    secret_name = "reddit_scraper"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return json.loads(secret)


def initialize_reddit_client():
    secret = get_secret()
    reddit = praw.Reddit(
        client_id=secret['client_id'],
        client_secret=secret['client_secret'],
        password=secret['user_password'],
        user_agent=secret['user_agent'],
        username=secret['username'],
    )
    return reddit


def initialize_prompt(response):

    reddit_post = response['title'] + '\n\n' + response['body'] if response['body'] else response['title']

    user_prompt = f"""### Instruction:
Respond to this Reddit post with an award winning top comment.

### Reddit Post:
{reddit_post}

### Image Context:\n"""

    return user_prompt


def format_image_context(image_caption, celebrities, detected_texts):

    image_context = f"""- Description:{image_caption}\n-Text:{detected_texts}\n-Celebrities:{celebrities}\n\n"""

    return image_context


def finalize_prompt(base_prompt, image_context):

    final_prompt = base_prompt + image_context + """### Response:\n"""

    return final_prompt


def download_image(image_id, image_url):

    local_filename = f"/tmp/image_{image_id}{image_url[-4:]}"
    urlretrieve(image_url, local_filename)

    return local_filename


def upload_image_to_s3(bucket_name, image_path):
    object_key = f"reddit/funny/inference/posts/{os.path.basename(image_path)}"
    s3.upload_file(image_path, bucket_name, object_key)
    return object_key


def generate_caption_from_s3(bucket_name, object_key, endpoint_name):
    """Generate a caption for the image using a BLIP model hosted on SageMaker"""

    # Initialize the SageMaker runtime client
    runtime = boto3.client('sagemaker-runtime')

    # Get the object from S3
    try:
        # Instead of loading the image into PIL, we'll directly send the image bytes to the SageMaker endpoint
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        image_bytes = response['Body'].read()

        # Prepare the payload for SageMaker endpoint - the specifics depend on how the model expects the input
        # For example, if your model expects JSON payload, you might need to base64 encode the image bytes.
        # Here, we assume the endpoint can directly take the image bytes.
        payload = image_bytes

        # Invoke the SageMaker endpoint
        # The ContentType in the invoke_endpoint call should match what your model expects.
        # This example uses 'application/x-image', but if your model expects a JSON payload with
        # a base64-encoded image, you'll need to adjust both the payload preparation and content type accordingly.
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           ContentType='application/x-image',  # Adjust if your model expects a different content type
                                           Body=payload)

        # Parse the result - adjust this based on how your model returns the caption
        result = json.loads(response['Body'].read().decode())

        return result['caption']  # Adjust this key based on your model's response structure

    except Exception as e:
        print(str(e))
        return "Error generating caption"


def get_celebrity_text(bucket_name, object_key):

    # Initialize the Rekognition client
    rekognition = boto3.client('rekognition')

    # Call Rekognition for Celebrity Recognition
    celebrity_response = rekognition.recognize_celebrities(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
    )
    celebrities = [celeb['Name'] for celeb in celebrity_response['CelebrityFaces']]
    celebrities = ', '.join(celebrities)

    # Call Rekognition for Text Detection
    text_response = rekognition.detect_text(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
    )
    detected_texts = [text_detection['DetectedText'] for text_detection in text_response['TextDetections']]
    detected_texts = ' '.join(detected_texts)

    return celebrities, detected_texts


def get_llama_response(endpoint_name, text_input):
    """Generate a response using the Llama model hosted on a SageMaker endpoint."""

    # Initialize the SageMaker runtime client
    runtime = boto3.client('sagemaker-runtime')

    # Prepare the payload for the SageMaker endpoint
    payload = {
        "inputs": text_input,
        "parameters": {
            "max_new_tokens": 64,
            "top_p": 0.9,
            "temperature": 0.6,
        },
    }

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload)

    try:
        # Invoke the SageMaker endpoint
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           ContentType='application/json',  # Specify the content type for your payload
                                           Body=payload_json)

        # Parse the response from the endpoint
        result = json.loads(response['Body'].read().decode())

        # Return the generated text. Adjust the key based on your model's specific response format.
        return result.get("generated_text", "No response generated")

    except Exception as e:
        print(f"Error invoking SageMaker endpoint: {str(e)}")
        return "Error generating response"

# Example usage:
# endpoint_name = 'your-llama-model-endpoint-name'
# text_input = "I believe the meaning of life is"
# print(get_llama_response(endpoint_name, text_input))