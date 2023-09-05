import torch
import whisper
import queue
import speech_recognition as sr
import threading
import io
import numpy as np
from pydub import AudioSegment
import wave
import os
import tempfile
import time
import platform
import pynput.keyboard
from pyannote.audio import Pipeline

#from whisper_mic.utils import get_logger

"""
This code was taken from mallorbs's whisper_mic repo 
**We did not write this**
source: https://github.com/mallorbc/whisper_mic/tree/main
"""

class WhisperMic:
    def __init__(self,model="base",device=("cuda" if torch.cuda.is_available() else "cpu"),english=False,verbose=False,energy=300,pause=0.8,dynamic_energy=False,save_file=False, model_root="./whisper_model",mic_index=None):
        #self.logger = get_logger("whisper_mic", "info")
        self.energy = energy
        self.pause = pause
        self.dynamic_energy = dynamic_energy
        self.save_file = save_file
        self.verbose = verbose
        self.english = english
        self.keyboard = pynput.keyboard.Controller()
        self.speaker_mapping = {}
        self.next_speaker_label = 'A'

        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="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")

        self.platform = platform.system()

        if self.platform == "darwin":
            if device == "mps":
                #self.logger.warning("Using MPS for Mac, this does not work but may in the future")
                device = "mps"
                device = torch.device(device)

        if (model != "large" and model != "large-v2") and self.english:
            model = model + ".en"
        
        self.audio_model = whisper.load_model(model, download_root=model_root).to(device)
        self.temp_dir = tempfile.mkdtemp() if save_file else None

        self.audio_queue = queue.Queue()
        self.result_queue: "queue.Queue[str]" = queue.Queue()

        self.break_threads = False
        self.mic_active = False

        self.banned_results = [""," ","\n",None]

        self.setup_mic(mic_index)



    def setup_mic(self, mic_index):
        if mic_index is None:
            pass#self.logger.info("No mic index provided, using default")
        self.source = sr.Microphone(sample_rate=16000, device_index=mic_index)

        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy
        self.recorder.pause_threshold = self.pause
        self.recorder.dynamic_energy_threshold = self.dynamic_energy

        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

        self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=2)
        #self.logger.info("Mic setup complete, you can now talk")


    def preprocess(self, data):
        return torch.from_numpy(np.frombuffer(data, np.int16).flatten().astype(np.float32) / 32768.0)

    def get_all_audio(self, min_time: float = -1.):
        audio = bytes()
        got_audio = False
        time_start = time.time()
        while not got_audio or time.time() - time_start < min_time:
            while not self.audio_queue.empty():
                audio += self.audio_queue.get()
                got_audio = True

        data = sr.AudioData(audio,16000,2)
        data = data.get_raw_data()
        return data
    
    def get_next_speaker_label(self):
        label = f"Speaker {self.next_speaker_label}"
        if self.next_speaker_label == 'Z':
            # Reset to A if we reach Z (you might want to handle this differently in a real scenario)
            self.next_speaker_label = 'A'
        else:
            self.next_speaker_label = chr(ord(self.next_speaker_label) + 1)
        return label



    def record_callback(self,_, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        self.audio_queue.put_nowait(data)


    def transcribe_forever(self) -> None:
        while True:
            if self.break_threads:
                break
            self.transcribe()


    def transcribe(self,data=None, realtime: bool = False) -> None:
        if data is None:
            audio_data = self.get_all_audio()
        else:
            audio_data = data
        audio_data = self.preprocess(audio_data)
        if self.english:
            result = self.audio_model.transcribe(audio_data,language='english')
        else:
            result = self.audio_model.transcribe(audio_data)

        predicted_text = result["text"]
        if not self.verbose:
            if predicted_text not in self.banned_results:
                self.result_queue.put_nowait(predicted_text)
        else:
            if predicted_text not in self.banned_results:
                self.result_queue.put_nowait(result)

        if self.save_file:
            os.remove(audio_data)


    def listen_loop(self, dictate: bool = False) -> None:
        threading.Thread(target=self.transcribe_forever).start()
        while True:
            result = self.result_queue.get()
            if dictate:
                self.keyboard.type(result)
            else:
                print(result)
    
    @staticmethod
    def extract_segment_from_audio(audio_path, segment):
        """Extracts segment from an audio file and returns raw audio data"""
        with wave.open(audio_path, 'rb') as wf:
            start_frame = int(segment.start * wf.getframerate())
            end_frame = int(segment.end * wf.getframerate())
            wf.setpos(start_frame)
            frames = wf.readframes(end_frame - start_frame)
            return frames


    # def listen(self, timeout: int = 3):
    #     print("listening...")
    #     audio_data = self.get_all_audio(timeout)

    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
    #         wf = wave.open(temp_wav.name, 'wb')
    #         wf.setnchannels(1)
    #         wf.setsampwidth(2)
    #         wf.setframerate(16000)
    #         wf.writeframes(audio_data)
    #         wf.close()

    #     diarization = self.pipeline(temp_wav.name)
    #     # Transcribe each segment and combine with speaker labels
    #     transcriptions = []
    #     for track in diarization.itertracks(yield_label=True):
    #         segment, speaker, *_ = track  # this will capture and ignore additional returned values
    #         segment_data = self.extract_segment_from_audio(temp_wav.name, segment)
    #         print("transcribing...")
    #         self.transcribe(data=segment_data)
    #         while True:
    #             if not self.result_queue.empty():
    #                 transcription = self.result_queue.get()
    #                 transcriptions.append((speaker, transcription))
    #                 break

    

    # # Printing the results
    #     for speaker, transcription in transcriptions:
    #         print(f"Speaker {speaker}: {transcription}")

    #     return transcriptions

    def listen(self, timeout = 3):
        audio_data = self.get_all_audio(timeout)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            wf = wave.open(temp_wav.name, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data)
            wf.close()

        try:
            diarization = self.pipeline(temp_wav.name)
        except Exception as e:
            print(f"Error in diarization: {e}")
            return None

        results = {}
        transcriptions = []

        for track in diarization.itertracks(yield_label=True):
            segment, speaker, *_ = track  # this will capture and ignore additional returned values
            segment_data = self.extract_segment_from_audio(temp_wav.name, segment)
            print("transcribing...")
            self.transcribe(data=segment_data)
            print("transcribed")
            while True:
                if not self.result_queue.empty():
                    transcription = self.result_queue.get()
                    # Check if the speaker_id has been mapped before, if not assign the next available label
                    if speaker not in self.speaker_mapping:
                        self.speaker_mapping[speaker] = self.get_next_speaker_label()

                    labeled_speaker = self.speaker_mapping[speaker]
                    transcriptions.append((labeled_speaker, transcription))
                    break
            print("done with loop")

        for labeled_speaker, transcription in transcriptions:
            results[labeled_speaker] = transcription

        return results


    
    # def toggle_microphone(self) -> None:
    #     #TO DO: make this work
    #     self.mic_active = not self.mic_active
    #     if self.mic_active:
    #         print("Mic on")
    #     else:
    #         print("turning off mic")
    #         self.mic_thread.join()
    #         print("Mic off")