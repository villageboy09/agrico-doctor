import os
import google.generativeai as genai
import streamlit as st
from PIL import Image
import io

# Set the environment variable for API key
os.environ["API_KEY"] = "AIzaSyCroPtzjFYNxHBuf_f-S_10cxu-B9TBhQI"

# Configure the API
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables.")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to upload an image using File API
def upload_image(image_file):
    try:
        image = Image.open(image_file)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)

        # Save the image to a temporary file
        temp_path = '/tmp/temp_image.png'
        with open(temp_path, 'wb') as f:
            f.write(image_bytes.read())

        # Upload the image using File API
        response = genai.upload_file(path=temp_path, display_name="Uploaded Image")
        return response.uri
    except Exception as e:
        st.error(f"Error uploading image: {e}")
        return None

# Function to analyze image and get recommendations
def analyze_image(image_uri):
    try:
        response = model.generate_content([image_uri, 'Identify any crop diseases and provide recommendations.'])
        return response.text
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
