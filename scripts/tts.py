import os
import uuid

from elevenlabs.client import ElevenLabs

from scripts.gpt import conf

# from scripts.translate import translate

elevenlabs = ElevenLabs(api_key=conf["tts_key"])

model = conf["model"]
TEMP_DIR = "temp"


def play_tts(text):
    os.makedirs(TEMP_DIR, exist_ok=True)
    audio = elevenlabs.text_to_speech.convert(
        output_format="mp3_22050_32",
        text=text,
        voice_id=conf["voice_id"],
        model_id=conf["model_id"],
    )

    file_name = f"{uuid.uuid4()}.wav"
    save_file_path = os.path.join(TEMP_DIR, file_name)
    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)

    return save_file_path
