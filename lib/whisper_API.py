import openai
import speech_recognition as sr

class Whisper_API:

    def transcribe(self, timout=3):
        pass


    def setup_mic(self, mic_index=None):
        if mic_index is None:
            pass  # self.logger.info("No mic index provided, using default")
        self.source = sr.Microphone(sample_rate=16000, device_index=mic_index)

        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy
        self.recorder.pause_threshold = self.pause
        self.recorder.dynamic_energy_threshold = self.dynamic_energy

        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

        self.recorder.listen_in_background(
            self.source, self.record_callback, phrase_time_limit=2)
    