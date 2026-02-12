import os
import re
from gtts import gTTS
from datetime import datetime


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def clean_text_for_speech(text: str) -> str:
    """
    Clean markdown symbols and format text for natural speech.
    """

    # Remove markdown bold/italics
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)

    # Replace bullet points with pauses
    text = text.replace("\n\n", ". ")
    text = text.replace("\n", ". ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def text_to_speech_and_save(text: str) -> str:
    """
    Convert cleaned text to speech and save as MP3.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean the text
    cleaned_text = clean_text_for_speech(text)

    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"response_{timestamp}.mp3"
    file_path = os.path.join(OUTPUT_DIR, filename)

   # Limit text length (gTTS works better with smaller chunks)
    MAX_LENGTH = 40000000000000000000

    if len(cleaned_text) > MAX_LENGTH:
        cleaned_text = cleaned_text[:MAX_LENGTH]

    tts = gTTS(text=cleaned_text, lang="en")
    tts.save(file_path)


    return file_path
