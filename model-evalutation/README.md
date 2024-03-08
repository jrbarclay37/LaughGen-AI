## Image Captioning Model Evaluation

I evaluated several models from huggingface's top [image-to-text models](https://huggingface.co/models?pipeline_tag=image-to-text):
a) [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)
b) [Salesforce/blip-image-captioning-large](https://huggingface.co/Salesforce/blip-image-captioning-large)
c) [nlpconnect/vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning)

In order to make a selection, I wanted to test for several areas of competence: 
- Can it accurately identify what is pictured? (this one is pretty important)
- What is the level of detail in the caption?
- Can it capture text?
- Can it recognize celebrities?
- Can it capture emotion?

### Image 1: African Savanna
![savanna](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/Savanna.png?raw=true)


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
