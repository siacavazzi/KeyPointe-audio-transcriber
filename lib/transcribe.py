from lib.whisper_API import Whisper_API
from lib.conversation import Conversation
from fuzzywuzzy import fuzz
import asyncio
import queue
import threading

class Transcriber:  
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.recording = True
        self.conversation = Conversation()

    def handle_row(self, row):
        self.conversation.add_row(row)


    @classmethod
    def is_end_command(cls, transcribed_text, threshold=90):
        """Check if the transcribed_text contains a sequence similar to 'end transcription'."""
        similarity = fuzz.partial_ratio(transcribed_text.lower(), "end transcription")
        return similarity >= threshold

    async def transcribe_from_queue(self, loop):
        while self.recording: 
            try:
                audio = self.audio_queue.get_nowait()
            except queue.Empty:
                await asyncio.sleep(1)
                continue
        
            res = await Whisper_API.get_transcript(audio)
            if Transcriber.is_end_command(res):
                self.recording = False
                loop.stop()
            print(res)
            self.handle_row(res)
    
    def record_audio(self):
        while self.recording:
            audio = Whisper_API.record_audio(3)
            self.audio_queue.put(audio)

    def run_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.create_task(self.transcribe_from_queue(loop))
        print("========== Listening... ==========")
        try:
            loop.run_forever()
        finally:
            print("============ Ended ============")
            print("Loading...")
            self.conversation.end_conversation()




 