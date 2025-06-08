import argparse
import random
from pathlib import Path
from openai import OpenAI
import os

# 可選的 voice 名稱（從圖片中擷取）
VOICES = [
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "onyx",
    "nova",
    "sage",
    "shimmer",
    "verse"
]

def generate_speech(input_text, instructions, output_path):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech_file_path = Path(output_path)

    selected_voice = random.choice(VOICES)
    print(f"Selected voice: {selected_voice}")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=selected_voice,
        input=input_text,
        instructions=instructions,
    ) as response:
        response.stream_to_file(speech_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate speech from text.")
    parser.add_argument("input", type=str, help="The text input to be converted to speech.")
    parser.add_argument("instructions", type=str, help="Instructions on how to speak the text (e.g., tone, emotion).")
    parser.add_argument("output_path", type=str, help="The file path where the speech audio will be saved.")

    args = parser.parse_args()

    generate_speech(args.input, args.instructions, args.output_path)