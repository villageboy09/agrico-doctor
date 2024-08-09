# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io

# Configure the API key
genai.configure(api_key=os.environ["AIzaSyCroPtzjFYNxHBuf_f-S_10cxu-B9TBhQI"])

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

# Function to upload an image
def upload_image(image_file):
    image = Image.open(image_file)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes.seek(0)
    response = genai.upload_file(file=image_bytes, display_name="Uploaded Image")
    return response.uri

# Function to analyze image and get recommendations
def analyze_image(image_uri):
    response = model.generate_content([image_uri, 'Identify any crop diseases and provide recommendations.'])
    return response.text

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
        recommendations = analyze_image(image_uri)
        st.subheader('Recommendations')
        st.write(recommendations)
    except Exception as e:
        st.error(f"An error occurred: {e}")
