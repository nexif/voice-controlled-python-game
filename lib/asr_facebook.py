import speech_recognition as sr


def asr_facebook(asr_model):
    pipe = asr_model

    try:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Recording...')
            audio = r.record(source, duration=1.5)
            with open("recording.wav", "wb+") as f:
                f.write(audio.get_wav_data())
        print('Transcribing...')
        result = pipe("recording.wav")
        text = result['text'].lower()
        print(text)
        return text
    except sr.UnknownValueError:
        return ''
