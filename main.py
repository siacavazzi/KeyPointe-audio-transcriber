from lib.whisper_mic import WhisperMic
from lib import CONN, CURSOR
from lib.conversation import Conversation
from lib.GPTcontainer import get_completion
from fuzzywuzzy import fuzz

def is_end_command(transcribed_text, threshold=90):
    """Check if the transcribed_text contains a sequence similar to 'end transcription'."""
    
    similarity = fuzz.partial_ratio(transcribed_text.lower(), "end transcription")
    return similarity >= threshold




# gpt = get_completion("hello")
# print(gpt)


mic = WhisperMic(english=True, model="small")
current_convo = Conversation()
while True:
    result = mic.listen()
    print(result)
    if is_end_command(result):
        break
    current_convo.add_row(result)


print("ENDED ---")



 