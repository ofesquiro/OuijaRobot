import pyaudio
import numpy as np
import noisereduce as nr
import scipy
from pocketsphinx import AudioFile, get_model_path
import os

MODEL_PATH = get_model_path()
LANGUAGE_PATH = "es-ES"
p : pyaudio.PyAudio = pyaudio.PyAudio()
format: int = pyaudio.paInt16
channel: int = 1
rate: int = 16000
chunk: int = 1024
stream: pyaudio._Stream = p.open(format=format,channels=channel,rate=rate,input=True,frames_per_buffer=chunk)

config : dict[str, any] = {
    'verbose': False,
    'audio_source': None,
    'hmm': os.path.join(MODEL_PATH, LANGUAGE_PATH),
    'lm': os.path.join(MODEL_PATH, 'en-us.lm.bin'),
    'dict': os.path.join(MODEL_PATH, 'cmudict-en-us.dict')
}



frames: list = []
for _ in range(0, int(rate / chunk * 5)):
    data: bytes = stream.read(chunk)
    frames.append(np.frombuffer(data, dtype=np.int16))
    
stream.stop_stream()
stream.close()
p.terminate()

# Convert frames to numpy array
audio_data = np.hstack(frames)

reduced_noise = nr.reduce_noise(y=audio_data, sr=rate)