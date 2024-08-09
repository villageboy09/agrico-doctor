import os
import requests
from PIL import Image
import streamlit as st
from io import BytesIO

# Set the environment variable for API key
os.environ["API_KEY"] = "AIzaSyCroPtzjFYNxHBuf_f-S_10cxu-B9TBhQI"

# Configure the API
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables.")

# Define supported crops
SUPPORTED_CROPS = [
    "tomato", "chilli", "paddy", "pearl millet", 
    "sorghum", "wheat", "maize", "groundnut", 
    "soybean", "sugarcane"
]

# Function to process the image using Pillow
def process_image_with_pillow(image_file):
    # Open image using PIL
    image = Image.open(image_file).convert("RGB")
    
    # Example processing: Convert to grayscale
    processed_image = image.convert("L")
    
    return processed_image

# Function to upload an image and return the file URI
def upload_image(image_file):
    try:
        # Process the image with Pillow
        processed_image = process_image_with_pillow(image_file)
        
        # Save the processed image to a temporary file
        temp_path = '/tmp/temp_image.png'
        processed_image.save(temp_path)

        # Upload the image using requests
        url = "https://generativeai.googleapis.com/v1/files:upload"
        headers = {"Authorization": f"Bearer {api_key}"}
        files = {'file': open(temp_path, 'rb')}
        response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            file_uri = response.json().get('uri')
            return file_uri
        else:
            st.error(f"Failed to upload image. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error uploading image: {e}")
        return None

# Function to analyze image and get recommendations
def analyze_image(image_uri):
    try:
        # Create a prompt based on supported crops
        prompt = (
            "Identify any crop diseases from the uploaded image and provide recommendations for the following crops: "
            + ", ".join(SUPPORTED_CROPS) + "."
        )
        url = "https://generativeai.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "content": [image_uri, prompt]
        }
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', 'No recommendations found.')
        else:
            st.error(f"Failed to analyze image. Status code: {response.status_code}")
            return "Unable to generate recommendations."
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        return "Unable to generate recommendations."

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
        if image_uri:
            recommendations = analyze_image(image_uri)
            st.subheader('Recommendations')
            st.write(recommendations)
        else:
            st.error("Failed to upload image. Please try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
else:
    st.info("Please upload an image file.")
