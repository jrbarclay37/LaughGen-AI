## Image Captioning Model Evaluation

I evaluated several models from huggingface's top [image-to-text models](https://huggingface.co/models?pipeline_tag=image-to-text):
1. [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)
2. [Salesforce/blip-image-captioning-large](https://huggingface.co/Salesforce/blip-image-captioning-large)
3. [nlpconnect/vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning)

In order to make a selection, I wanted to test for several areas of competence: 
- Can it accurately identify what is pictured? (this one is pretty important)
- What is the level of detail in the caption?
- Can it capture text?
- Can it recognize celebrities?
- Can it capture emotion?

### Image 1: African Savanna
![savanna](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/Savanna.png?raw=true)
`BLIP-base` 
*"a bus is parked at an airport with a plane in the background"*
`BLIP-large`
*"there are many buses and buses parked at the airport"*
`VIT-GPT2`
*"a large jetliner sitting on top of an airport tarmac"*

### Image 2: Soccer Players
![soccer](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/soccer_player.png?raw=true)


### Image 3: Road Sign
![road-sign](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/sign_with_text.png?raw=true)


### Image 4: Car with Bumper Stickers
![car-stickers](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/car_stickers.png?raw=true)


### Image 5: Tractor Collection
![tractor-collection](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/tractor_text.png?raw=true)


### Image 6: John Wick
![john-wick](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/Keanu.png?raw=true)


### Image 7: Woman Pleading
![woman-pleading](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/woman_pleading.png?raw=true)
