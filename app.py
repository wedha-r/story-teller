import streamlit as st
import requests
import base64
from io import BytesIO
import os
from gtts import gTTS
from PIL import Image
import random

# AI Studios API Configuration
AI_STUDIOS_API_KEY = "YOUR_AISTUDIOS_API_KEY"
TEXT_GEN_URL = "https://api.aistudios.com/text-generation"
TTS_URL = "https://api.aistudios.com/text-to-speech"
IMAGE_GEN_URL = "https://api.aistudios.com/image-generation"

# Function to generate story
def generate_story(title, theme, age_group, num_lines):
    prompt = f"Write a {num_lines}-line story titled '{title}' with the theme '{theme}' for a {age_group} audience."
    payload = {"prompt": prompt, "max_tokens": 200}
    headers = {"Authorization": f"Bearer {AI_STUDIOS_API_KEY}"}
    response = requests.post(TEXT_GEN_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("text", "Story generation failed.")
    return "Error generating story."

# Function to convert text to speech
def text_to_speech(story_text):
    tts = gTTS(text=story_text, lang="en")
    audio_path = "story.mp3"
    tts.save(audio_path)
    return audio_path

# Function to generate related image
def generate_image(title, theme):
    payload = {"prompt": f"An illustration for a {theme} story titled '{title}'."}
    headers = {"Authorization": f"Bearer {AI_STUDIOS_API_KEY}"}
    response = requests.post(IMAGE_GEN_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        image_data = base64.b64decode(response.json()["image_base64"])
        img = Image.open(BytesIO(image_data))
        img_path = "story_image.png"
        img.save(img_path)
        return img_path
    return None

# Function to get background music
def get_background_music(theme):
    theme_music = {
        "Adventure": "adventure_music.mp3",
        "Fantasy": "fantasy_music.mp3",
        "Horror": "horror_music.mp3",
        "Sci-Fi": "sci_fi_music.mp3",
        "Kids": "kids_music.mp3"
    }
    return theme_music.get(theme, "default_music.mp3")

# Streamlit UI
st.title("AI Storyteller")

title = st.text_input("Enter Story Title", "The Magic Forest")
theme = st.selectbox("Select Theme", ["Adventure", "Fantasy", "Horror", "Sci-Fi", "Kids"])
age_group = st.selectbox("Select Age Group", ["Kids", "Teenagers", "Adults"])
num_lines = st.slider("Number of Lines", min_value=5, max_value=50, value=10)

if st.button("Generate Story"):
    story = generate_story(title, theme, age_group, num_lines)
    st.write("### Generated Story")
    st.write(story)

    audio_file = text_to_speech(story)
    image_file = generate_image(title, theme)
    music_file = get_background_music(theme)

    if image_file:
        st.image(image_file, caption="Story Illustration")

    st.audio(audio_file, format="audio/mp3")
    st.audio(music_file, format="audio/mp3", autoplay=True)
