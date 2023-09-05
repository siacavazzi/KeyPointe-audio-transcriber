from whisper_mic import WhisperMic

mic = WhisperMic(english=True, model="small")
while True:
    result = mic.listen()
    print(result)