import speech_recognition as sr


def asr_whisper(asr_model):
    model = asr_model

    try:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Recording...')
            audio = r.record(source, duration=1.5)
            with open("recording.wav", "wb+") as f:
                f.write(audio.get_wav_data())
        print('Transcribing...')
        result = model.transcribe(
            'recording.wav', fp16=False, language="pl", initial_prompt='góra dół lewo prawo')
        text = result['text'].lower()
        print(text)
        return text
    except sr.UnknownValueError:
        return ''
