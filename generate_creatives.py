import requests
import base64
import boto3
from PIL import Image
from io import BytesIO
import json
import os
import streamlit as st

import uuid

AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = st.secrets["AWS_CREATIVES_REGION"]
IMAGE_API = st.secrets["IMAGE_API"]

url = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"

def upload_to_s3(encoded_data, image_dir, image_name, Delete=False, Create=False):

    image = Image.open(BytesIO(encoded_data))
    png_image_buffer = BytesIO()
    image.save(png_image_buffer, format="PNG")
    png_image_buffer.seek(0)
    
    if Create:
        os.makedirs(image_dir, exist_ok=True)
        
    image_path = os.path.join(image_dir, image_name + '.png')
    
    if Create:
        with open(image_path, 'wb') as f:
            f.write(png_image_buffer.getbuffer())
    
    client = boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    

    bucket_name = 'cannes-demo'
    object_key = os.path.join(image_dir, image_name + '.png')
    

    png_image_buffer.seek(0)
    client.put_object(Bucket=bucket_name, Key=object_key, Body=png_image_buffer)
    
    
    if Delete and os.path.exists(image_path):
        os.remove(image_path)
    
    print('Image uploaded successfully')


def generate_img_1(prompt, image_dir, Delete, Create):
    payload = {
    "model": "stable-diffusion-v1-5",
    "style": "anime",
    "prompt": prompt,
    "width": 960,
    "height": 256,
    "output_format": "jpeg"
    }

    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": IMAGE_API
    }

    response = requests.post(url, json=payload, headers=headers)
    image_name = "image_1"
    if response.status_code == 200:
        data = response.json()
        img_data = base64.b64decode(data['image'])
        upload_to_s3(img_data, image_dir, image_name, Delete, Create)
        return "Success"
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        print(response.text)
        return "Failure"

def generate_img_2(prompt, image_dir, Delete, Create):
    payload = {
    "model": "stable-diffusion-v1-5",
    "style": "anime",
    "prompt": prompt,
    "width": 320,
    "height": 640,
    "output_format": "jpeg"
    }
    image_name = "image_2"
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": IMAGE_API
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        img_data = base64.b64decode(data['image'])
        upload_to_s3(img_data, image_dir, image_name, Delete, Create)
        return "Success"
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        print(response.text)
        return "Failure"

def generate_img_3(prompt, image_dir, Delete, Create):
    payload = {
    "model": "stable-diffusion-v1-5",
    "style": "anime",
    "prompt": prompt,
    "width": 320,
    "height": 256,
    "output_format": "jpeg"
    }
    image_name = "image_3"
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": IMAGE_API
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        img_data = base64.b64decode(data['image'])
        upload_to_s3(img_data, image_dir, image_name, Delete, Create)
        return "Success"
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        print(response.text)
        return "Failure"


def store_image_1(prompt, image_dir):
    image_1 = generate_img_1(prompt, image_dir, Delete = True, Create = True)

def store_image_2(prompt, image_dir):
    image_2 = generate_img_2(prompt, image_dir, Delete = False, Create = False)

def store_image_3(prompt, image_dir):
    image_3 = generate_img_3(prompt, image_dir, Delete = False, Create = False)