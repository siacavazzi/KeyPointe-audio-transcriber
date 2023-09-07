from .whisper_mic import WhisperMic
from .conversation import Conversation
from fuzzywuzzy import fuzz

def is_end_command(transcribed_text, threshold=90):
    """Check if the transcribed_text contains a sequence similar to 'end transcription'."""
    similarity = fuzz.partial_ratio(transcribed_text.lower(), "end transcription")
    return similarity >= threshold

def transcribe_speech():
    print("Loading...")
    mic = WhisperMic(english=True, model="small")
    current_convo = Conversation()
    print("====================================== Listening... ======================================")
    while True:
        result = mic.listen()
        if len(result) != 0 and result != "Thanks for watching!": # for some reason when its quiet whisper hallucinates thanks for watching
            print(result)
            if is_end_command(result):
                break
            current_convo.add_row(result)
        
    print("=================================== Transcription Ended ===================================")
    print("Wrapping up...")
    current_convo.end_conversation()
    




 