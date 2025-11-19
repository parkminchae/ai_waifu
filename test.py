import scipy.io.wavfile
import sounddevice as sd

from scripts.tts import save_tts

audio_path = save_tts("오늘 팬티 뭐입었어?")

print(audio_path)

v_samplerate, v_data = scipy.io.wavfile.read(audio_path)
sd.play(v_data, v_samplerate)
sd.wait()
