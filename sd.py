import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import os
import sys
from imgkit import upload

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

current_path = sys.path[0]
output_dir = os.path.join(current_path,'outputs')

default_prompt = "RAW photo, subject, (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3,"
negative_prompt = "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation, UnrealisticDream"


def generateImage(prompt,seed=-1,width=600,height=800):

    payload = json.dumps({
        "enable_hr": False,
        "denoising_strength": 0.7,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "prompt":default_prompt + prompt,
        "styles": [
          ""
        ],
        "seed": seed,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "DPM++ SDE Karras",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 25,
        "cfg_scale": 7,
        "width": width,
        "height": height,
        "restore_faces": False,
        "tiling": False,
        "negative_prompt":negative_prompt,
        "eta": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "script_args": [],
        "sampler_index": "DPM++ SDE Karras"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    r = response.json()
    info = json.loads(r['info'])
    prompt = info['prompt']
    seed = info['subseed']

    for index,i in enumerate(r['images']):
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_binary = img_bytes.getvalue()
              
        url = upload(img_binary)        
        return url



if __name__ == "__main__":    
    generateImage(prompt=prompt, seed=-1, width=600, height=800)
    
