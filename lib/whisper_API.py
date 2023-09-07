import openai
import sounddevice as sd
import numpy as np
import wavio
import tempfile
from lib.apiKey import key
import asyncio

class Whisper_API:

    @classmethod
    async def get_transcript(cls, audio_file_path, timout=3):
        openai.api_key = key
        audio = open(audio_file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio)
        return transcript.text


    def record_audio(duration, samplerate=44100):
        # Record audio for the specified duration
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        # Save the audio data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            wavio.write(temp_wav.name, audio_data, samplerate)
            return temp_wav.name


