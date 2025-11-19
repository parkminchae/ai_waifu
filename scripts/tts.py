import os
import uuid

from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

from scripts.gpt import conf

# from scripts.translate import translate

elevenlabs = ElevenLabs(api_key=conf["tts_key"])

model = conf["model"]
TEMP_DIR = "temp"


def save_tts(text):

    os.makedirs(TEMP_DIR, exist_ok=True)

    # Get MP3 audio data

    audio = elevenlabs.text_to_speech.convert(
        output_format="mp3_44100_128",
        text=text,
        voice_id=conf["voice_id"],
        model_id=conf["model_id"],
    )

    # Save as temporary MP3

    temp_mp3 = f"{uuid.uuid4()}.mp3"

    temp_mp3_path = os.path.join(TEMP_DIR, temp_mp3)

    with open(temp_mp3_path, "wb") as f:

        for chunk in audio:

            if chunk:

                f.write(chunk)

    # Convert MP3 to WAV

    audio_segment = AudioSegment.from_mp3(temp_mp3_path)

    file_name = f"{uuid.uuid4()}.wav"

    save_file_path = os.path.join(TEMP_DIR, file_name)

    audio_segment.export(save_file_path, format="wav")

    # Clean up temporary MP3

    os.remove(temp_mp3_path)

    return save_file_path
