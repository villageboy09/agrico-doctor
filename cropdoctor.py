# -*- coding: utf-8 -*-
"""cropdoctor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11c8Y9809_O-lV1zyQY01YIVgLbeSbozn
"""

!pip install streamlit
import streamlit as st
import requests
from PIL import Image
import io

# Set up your API key and endpoints
API_KEY = 'AIzaSyCroPtzjFYNxHBuf_f-S_10cxu-B9TBhQI'
UPLOAD_ENDPOINT = 'https://api.gemini.ai/v1/media/upload'
ANALYZE_ENDPOINT = 'https://api.gemini.ai/v1/generate_content'

# Function to upload an image
def upload_image(image_file):
    response = requests.post(
        UPLOAD_ENDPOINT,
        headers={'Authorization': f'Bearer {API_KEY}'},
        files={'file': image_file}
    )
    response.raise_for_status()
    return response.json()['uri']

# Function to analyze image and get recommendations
def analyze_image(image_uri):
    response = requests.post(
        ANALYZE_ENDPOINT,
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        json={
            'model': 'gemini-1.5-pro',
            'prompts': [
                {
                    'image': image_uri,
                    'text': 'Identify any crop diseases and provide recommendations.'
                }
            ]
        }
    )
    response.raise_for_status()
    return response.json()

# Streamlit app interface
st.title('Crop Disease Detection and Recommendations')

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Upload image and analyze
    try:
        image_uri = upload_image(uploaded_file)
        analysis_result = analyze_image(image_uri)
        recommendations = analysis_result['results'][0]['text']
        st.subheader('Recommendations')
        st.write(recommendations)
    except Exception as e:
        st.error(f"An error occurred: {e}")

streamlit run cropdoctor.py