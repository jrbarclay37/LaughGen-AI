# LaughGen-AI
Multi-Modal Humor Generation for Reddit Posts

![funny-bot-wide](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/funny-bot-wide.png?raw=true)

## Table of Contents

- [Overview](#overview)
- [Data Enrichment and Preparation Pipeline](#data-enrichment-and-preparation-pipeline)
- [Supervised Fine-Tuning with PEFT](#supervised-fine-tuning-with-peft)
- [Deployment](#deployment)

## Overview

In this repository, I will be fine-tuning [Llama 2 13B](https://huggingface.co/meta-llama/Llama-2-13b) on top comments from submissions on the subreddit, r/funny.

Humor is a complex and subjective domain, and while language models can generate amusing content, their attempts often fall into the realm of predictably corny. Prompting can improve this, but it's difficult to emulate the level of wittiness of comments on r/funny that are so ridiculous they'll have you spewing your morning cup of coffee all over your keyboard. This project aims to bridge that gap, leveraging the unique humor of r/funny to bring a new level of comedic intelligence to Llama 2 13B.

## Data Enrichment and Preparation Pipeline
This is the most crucial part of the project and makes up for the bulk of the effort. In order to procure a high quality dataset that results in a good fine-tuned model the following steps are taken:
- Scrape *r/funny* using [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/stable/)
- Generate image descriptions with [BLIP Image Captioning Model](https://huggingface.co/Salesforce/blip-image-captioning-large)
- Augment image descriptions with celebrity and text detection using [Amazon Rekognition](https://aws.amazon.com/rekognition/)
- Impute missing image descriptions with few-shot learning using [GPT-4](https://openai.com/gpt-4)

## Supervised Fine-Tuning with PEFT
Use QLoRA to fine-tune Llama 2 13B on the curated Reddit dataset.

## Deployment

### Phase I (Interact via API)
For this initial phase, I will deploy this system where users can submit the URL of a post from any subreddit and a witty comment will be returned. 

![api-gateway](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/model_results/api_gateway_method.png?raw=true)

![amazon-delivery-comment](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/model_results/amazon_delivery_comment.png?raw=true)

![amazon-delivery-post](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/model_results/amazon_delivery_french_bulldog.png?raw=true)


### Phase II (Reddit bot)
For this second phase, I will release a Reddit bot into the wild to make humorous comments on posts for numerous communities.
