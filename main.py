from lib.whisper_mic import WhisperMic
from lib import CONN, CURSOR
from lib.conversation import Conversation
from lib.GPTcontainer import get_completion
from fuzzywuzzy import fuzz
from lib.overview import Overview

def is_end_command(transcribed_text, threshold=90):
    """Check if the transcribed_text contains a sequence similar to 'end transcription'."""
    
    similarity = fuzz.partial_ratio(transcribed_text.lower(), "end transcription")
    return similarity >= threshold



mic = WhisperMic(english=True, model="small")
current_convo = Conversation()
while True:
    print("==== Listening... ====")
    result = mic.listen()
    print(f"no len filtering: {result}")
    if len(result) is not 0:
        print(result)
        if is_end_command(result):
            break
        current_convo.add_row(result)
        
print("ENDED ---")
current_convo.end_conversation()




 