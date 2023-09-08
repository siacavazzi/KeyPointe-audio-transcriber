from lib.whisper_API import Whisper_API
from lib.conversation import Conversation
from fuzzywuzzy import fuzz
import asyncio
import queue
from .title import listening, ended

class Transcriber:
    banned_phrases = ["thanks for watching","Thank you for watching.",
                      "Share this video with your friends on social media.","시청해주셔서 감사합니다!",
                      "ご視聴ありがとうございました"]

    def __init__(self, timout=3):
        self.audio_queue = queue.Queue()
        self.recording = True
        self.conversation = Conversation()
        self.timout = timout
        

    def handle_row(self, row):
        self.conversation.add_row(row)


    @classmethod
    def text_is_similar(cls, transcribed_text, target_text,threshold=90):
        """Check if the transcribed_text contains a sequence similar to target text."""
        similarity = fuzz.partial_ratio(transcribed_text.lower(), target_text)
        return similarity >= threshold
    
    @classmethod
    def is_banned_phrase(cls, transcribed_text):
        for phrase in cls.banned_phrases:
            if cls.text_is_similar(transcribed_text, phrase):
                return True
        return False


    async def transcribe_from_queue(self, loop):
        while self.recording: 
            try:
                audio = self.audio_queue.get_nowait()
            except queue.Empty:
                await asyncio.sleep(1)
                continue
        
            res = await Whisper_API.get_transcript(audio)
            if Transcriber.text_is_similar(res , "end transcription"):
                self.recording = False
                loop.stop()

            if Transcriber.is_banned_phrase(res):
                res = "[silence...]"
            print(res)
            self.handle_row(res)
    
    def record_audio(self):
        while self.recording:
            audio = Whisper_API.record_audio(self.timout)
            self.audio_queue.put(audio)

    def run_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.create_task(self.transcribe_from_queue(loop))
        print(listening)
        try:
            loop.run_forever()
        finally:
            print(ended)
            print("Loading...")
            self.conversation.end_conversation()




 