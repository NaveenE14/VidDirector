import os
import shutil
from clarifai.client.model import Model

def generate_images(image_model, image_prompts, clarifai_pat):
    if image_model == "DALLE3":
        USER_ID = 'openai'
        APP_ID = 'dall-e'
        MODEL_ID = 'dall-e-3'
    elif image_model == "IMAGEN":
        USER_ID = 'gcp'
        APP_ID = 'generate'
        MODEL_ID = 'Imagen'
    elif image_model == "STABLEDIFFUSION XL":
        USER_ID = 'stability-ai'
        APP_ID = 'stable-diffusion-2'
        MODEL_ID = 'stable-diffusion-xl'

    folder_path = "image"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    else:
        os.makedirs(folder_path)
    
    for idx, image_prompt in enumerate(image_prompts):
        prompt = image_prompt
        inference_params = dict(quality="standard", size='1024x1024')
        model_prediction = Model(f"https://clarifai.com/openai/dall-e/models/{MODEL_ID}", pat=clarifai_pat).predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
        output_base64 = model_prediction.outputs[0].data.image.base64
        image_filename = f"image/image_{idx}.jpg"   
        with open(image_filename, 'wb') as f:
            f.write(output_base64)
    print("Images generated successfully")