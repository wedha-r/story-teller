import streamlit as st
import openai
import os
import requests
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API Key for images
ai_studios_api_key = os.getenv("AI_STUDIOS_API_KEY")  # AI Studios API Key for text

import requests

def generate_story(prompt, theme, age_group, length):
    api_url = "YOUR_API_ENDPOINT"  # Replace with the correct API URL
    payload = {"prompt": prompt, "theme": theme, "age_group": age_group, "length": length}
    
    response = requests.post(api_url, json=payload)
    
    # Debugging: Print raw response
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)  # Print raw response text

    try:
        return response.json().get("story", "Story generation failed.")
    except requests.exceptions.JSONDecodeError:
        return "Error: Invalid JSON response from API."


def generate_image(prompt):
    """Generate an image based on the story prompt using OpenAI's DALL-E."""
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response["data"][0]["url"]
    return image_url

# Streamlit UI
st.title("AI Storyteller")
st.write("Enter a prompt, choose a theme, and let AI create a story for you!")

prompt = st.text_area("Enter your story prompt:")
theme = st.selectbox("Select a story theme:", ["Fantasy", "Romantic", "Horror", "Funny", "Adventure"])
age_group = st.selectbox("Select the target age group:", ["Children", "Teenagers", "Adults"])
length = st.selectbox("Select the length of the story:", ["Short", "Medium", "Long"])

if st.button("Generate Story and Image"):
    if prompt:
        story = generate_story(prompt, theme, age_group, length)
        st.subheader("Your Story:")
        st.write(story)
        
        # Generate and display image
        st.subheader("Story Illustration:")
        image_url = generate_image(f"{theme} story illustration of {prompt}")
        st.image(image_url, caption="Generated Story Image")
    else:
        st.warning("Please enter a prompt.")

# Instructions for VS Code:
# 1. Install dependencies: pip install streamlit openai python-dotenv pillow requests
# 2. Create a .env file and add:
#    OPENAI_API_KEY=your_openai_api_key_here
#    AI_STUDIOS_API_KEY=your_ai_stustorydios_api_key_here
# 3. Run the app using: streamlit run app.py
