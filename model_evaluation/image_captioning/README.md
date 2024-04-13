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
- `BLIP-base` 
*"a gi and zebra grazing in the savannah"*
- `BLIP-large`
*"zebras and giraffes in a field with trees and bushes"*
- `VIT-GPT2`
*"a herd of giraffes and zebras grazing in a field"*

The base model had a typo, but all models accurately described the picture.

### Image 2: Soccer Players
![soccer](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/soccer_player.png?raw=true)
- `BLIP-base` 
*"a soccer player in action with the ball"*
- `BLIP-large`
*"there are two men playing soccer on a field with a ball"*
- `VIT-GPT2`
*"a soccer player kicking a soccer ball"*

### Image 3: Road Sign
![road-sign](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/sign_with_text.png?raw=true)
- `BLIP-base` 
*"a street sign that says drive next"*
- `BLIP-large`
*"arafed sign on a pole on a street with cars parked on the side"*
- `VIT-GPT2`
*"a street sign on a pole in a rural area"*

### Image 4: Car with Bumper Stickers
![car-stickers](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/car_stickers.png?raw=true)
- `BLIP-base` 
*"a car with a license on it's back"*
- `BLIP-large`
*"arafed car with a sticker on the back of it"*
- `VIT-GPT2`
*"a car is parked on the side of the road"*

### Image 5: Tractor Collection
![tractor-collection](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/tractor_text.png?raw=true)
- `BLIP-base` 
*"a man and woman are working on a machine"*
- `BLIP-large`
*"there are two people standing in a room with a tractor"*
- `VIT-GPT2`
*"a woman and a man are standing in front of a display of bananas"*

### Image 6: John Wick
![john-wick](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/Keanu.png?raw=true)
- `BLIP-base` 
*"kersson as john in the walking dead"*
- `BLIP-large`
*"arafed man in a suit and tie looking at the camera"*
- `VIT-GPT2`
*"a man in a suit and tie"*

### Image 7: Woman Pleading
![woman-pleading](https://github.com/jrbarclay37/LaughGen-AI/blob/main/images/test_images/woman_pleading.png?raw=true)
- `BLIP-base` 
*"a woman is sitting at a table with her hands folded"*
- `BLIP-large`
*"woman with hands folded in prayer while sitting at a table"*
- `VIT-GPT2`
*"a woman is sitting on a wooden floor"*

## Conclusion


