from lib.whisper_mic import WhisperMic
from lib import CONN, CURSOR
from lib.conversation import Conversation

mic = WhisperMic(english=True, model="small")
Conversation.create_table()

current_convo = Conversation()
while True:
    results = mic.listen()
    print(results)
    for result in results:
        #current_convo.add_row(result)
        pass