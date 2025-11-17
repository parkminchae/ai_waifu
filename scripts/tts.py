from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

from scripts.gpt import conf

# from scripts.translate import translate

elevenlabs = ElevenLabs(api_key=conf["tts_key"])

model = conf["model"]


def play_tts(text):
    audio = elevenlabs.text_to_speech.convert(
        # text=translate(model, text),
        text=text,
        voice_id=conf["voice_id"],
        model_id=conf["model_id"],
        output_format="mp3_44100_128",
    )

    play(audio)
