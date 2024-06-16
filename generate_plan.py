import boto3
import os
import json
import streamlit as st
 
AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = st.secrets["AWS_CREATIVES_REGION"]

def call_bedrock_llama3(prompt, max_tokens=2048, temperature=0.4, top_p=0.9):
    client = boto3.client(
        'bedrock-runtime',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    payload = {
        'prompt': prompt,
        'max_gen_len': max_tokens,
        'temperature': temperature,
        'top_p': top_p
    }
    
    response = client.invoke_model(
        modelId='meta.llama3-8b-instruct-v1:0',
        contentType='application/json',
        accept='application/json',
        body=json.dumps(payload).encode('utf-8')
    )

    response_payload = response['body'].read()
    response_json = json.loads(response_payload)
    print("Full response from Bedrock API:", response_json)
    return response_json