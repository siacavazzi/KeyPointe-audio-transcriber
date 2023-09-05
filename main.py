from lib.whisper_mic import WhisperMic
from lib import CONN, CURSOR
from lib.conversation import Conversation

mic = WhisperMic(english=True, model="small")
while True:
    result = mic.listen()
    print(result)