from lib.whisper_mic import WhisperMic
from lib import CONN, CURSOR
from lib.conversation import Conversation

mic = WhisperMic(english=True, model="small")
Conversation.create_table()

current_convo = Conversation()

# gpt = mic.get_completion("hello")
# print(gpt)

while True:
    result = mic.listen()
    print(result)
    current_convo.add_row(result)
 