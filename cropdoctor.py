import os
import numpy as np
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

# Define supported crops
SUPPORTED_CROPS = [
    "tomato", "chilli", "paddy", "pearl millet", 
    "sorghum", "wheat", "maize", "groundnut", 
    "soybean", "sugarcane"
]

# Function to process the image using OpenCV
def process_image_with_opencv(image_file):
    # Open image using PIL and convert to OpenCV format
    image = Image.open(image_file).convert("RGB")
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    
    # Example processing: Convert to grayscale
    processed_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
    # Convert back to PIL Image format
    processed_image_pil = Image.fromarray(processed_image)
    return processed_image_pil

# Function to upload an image using File API
def upload_image(image_file):
    try:
        # Process the image with OpenCV
        processed_image = process_image_with_opencv(image_file)
        
        # Save the processed image to a temporary file
        temp_path = '/tmp/temp_image.png'
        processed_image.save(temp_path)

        # Upload the image using File API
        response = genai.upload_file(path=temp_path, display_name="Processed Image")
        return response.uri
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
        response = model.generate_content([image_uri, prompt])
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
else:
    st.info("Please upload an image file.")
