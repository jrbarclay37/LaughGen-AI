
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

def model_fn(model_dir):
    # Load model from HuggingFace Hub
    processor = BlipProcessor.from_pretrained(model_dir)
    model = BlipForConditionalGeneration.from_pretrained(model_dir)
    
    return model, processor

def predict_fn(data, model_and_processor):
    # Destruct model and tokenizer
    model, processor = model_and_processor
    
    # For debugging
    print(f"Received data type: {type(data)}")
    print(f"Received data content: {data}")
    
    # Check if 'inputs' key exists in the dictionary
    if 'inputs' in data:
        inputs = data['inputs']
        # Extract 'img_url' and 'text'
        img_url = inputs.get('img_url')
        text = inputs.get('text')
        max_new_tokens = inputs.get('max_new_tokens', 20)
        skip_special_tokens = inputs.get('skip_special_tokens', True) 
        # Raise error if 'img_url' is missing
        if img_url is None:
            raise ValueError("Dictionary is missing 'img_url' key. It should be formatted as {'inputs' : {'img_url' : '<URL>', 'text': '<Text>' }}")
    else:
        raise ValueError("Dictionary is missing 'inputs' key. It should be formatted as {'inputs' : {'img_url' : '<URL>', 'text': '<Text>' }}")
    
    # Load the image
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    # Conditional image captioning
    if text:
        inputs = processor(raw_image, text, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=max_new_tokens)
        caption = {'generated text' : processor.decode(out[0], skip_special_tokens=skip_special_tokens)}
    else:
        # Unconditional image captioning
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=max_new_tokens)
        caption = {'generated text' : processor.decode(out[0], skip_special_tokens=skip_special_tokens)}
        
    return caption
