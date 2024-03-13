import os
import io
import json
import boto3
import praw
from botocore.exceptions import ClientError
from urllib.request import urlretrieve

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('processed-reddit-submissions')

def lambda_handler(event, context):
    
    try:

        bucket_name = 'sagemaker-us-east-1-513033806411'

        blip_endpoint_name = "huggingface-pytorch-inference-2024-03-08-16-01-37-935"
        llm_endpoint_name = "huggingface-pytorch-tgi-inference-2024-03-08-17-46-49-268"

        # Initialize Reddit Client
        reddit = initialize_reddit_client()

        # get submissions for the last hour
        for submission in reddit.subreddit("funny").top(time_filter="hour"):

            # check processed-reddit-submissions table
            processed = check_and_process_submission(submission.id)
            if not processed:
                print(f"Skipping already processed submission: {submission.id}")
                continue  # Skip to the next submission if this one has been processed

            # Initialize response dictionary
            response = {
                "id": submission.id,
                "title": submission.title,
                "body": submission.selftext,
                "url": submission.url
            }

            prompt = initialize_prompt(response)

            # If there is an image, process it
            if submission.url.endswith(('.jpg', '.png', '.jpeg')):

                # Download the image to a temporary location
                image_path = download_image(submission.id, submission.url)

                # Upload the image to S3
                object_key = upload_image_to_s3(bucket_name, image_path)

                # Generate an image caption using the BLIP model
                image_caption = generate_image_caption(blip_endpoint_name, submission.url)
                celebrities, detected_texts = get_celebrity_text(bucket_name, object_key)

            else:
                # don't process
                continue

            # format image context
            image_context = format_image_context(image_caption, celebrities, detected_texts)

            #finalize prompt
            final_prompt = finalize_prompt(prompt, image_context)

            llama_params = {
                "max_new_tokens": 128,
                "top_p": 0.9,
                "temperature": 0.9,
                "stop": ["</s>"]
            }

            # Get a response from the Llama2 model using the post title and image caption
            llama_response = get_llama_response(llm_endpoint_name, final_prompt, llama_params)

            # retry
            if json.dumps(llama_response) == "[removed]":
                llama_params['temperature'] = 0.6
                llama_response = get_llama_response(llm_endpoint_name, final_prompt, llama_params)

            # decode unicode response
            generated_comment = decode_unicode_strings(json.dumps(llama_response))

            # submit comment
            print(generated_comment)
            submission.reply(generated_comment)

    except Exception as e:
        print(str(e))


def decode_unicode_strings(input_string):
    # Decode the Unicode escape sequences
    decoded_string = input_string.encode('utf-8').decode('unicode_escape')
    return decoded_string


def check_and_process_submission(submission_id):
    # Check if the submission has already been processed
    response = table.get_item(
        Key={'submissionId': submission_id}
    )
    if 'Item' in response:
        return False  # Submission has already been processed

    # Mark submission as processed
    table.put_item(
        Item={'submissionId': submission_id}
    )
    return True


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
        user_agent='LaughGen-AI by u/LaughGenBot',
        username='LaughGenBot',
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

    local_filename = f"/tmp/image_{image_id}{image_url.split('.')[1]}"
    urlretrieve(image_url, local_filename)

    return local_filename


def upload_image_to_s3(bucket_name, image_path):
    s3 = boto3.client('s3')
    object_key = f"reddit/funny/inference/posts/{os.path.basename(image_path)}"
    s3.upload_file(image_path, bucket_name, object_key)
    return object_key


def generate_image_caption(endpoint_name, img_url):


    # Create a SageMaker runtime client
    client = boto3.client('sagemaker-runtime')

    # Provide the payload you want to use for prediction
    data = {
        "inputs": {
            "img_url": img_url,
            "text" : "An image of ",
        }
    }
    payload = json.dumps(data)

    # Specify the content type and accept headers
    content_type = "application/json"
    accept = "application/json"

    # Invoke the endpoint
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType=content_type,
        Accept=accept,
        Body=payload
    )

    return response['Body'].read().decode()


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


def get_llama_response(endpoint_name, text_input, parameters):
    """Generate a response using the Llama model hosted on a SageMaker endpoint."""

    # Initialize the SageMaker runtime client
    client = boto3.client('sagemaker-runtime')

    # Prepare the payload for the SageMaker endpoint
    payload = {
        "inputs": text_input,
        "parameters": parameters,
    }

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload)

    # Invoke the SageMaker endpoint
    response = client.invoke_endpoint(EndpointName=endpoint_name,
                                       ContentType='application/json',  # Specify the content type for your payload
                                       Body=payload_json)

    # Parse the response from the endpoint
    result = json.loads(response['Body'].read().decode())

    # Return the generated text. Adjust the key based on your model's specific response format.
    return result[0].get("generated_text", "No response generated")
