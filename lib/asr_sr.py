import speech_recognition as sr


def asr_sr():
    init_rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = init_rec.record(source, duration=1.5)
        try:
            text = init_rec.recognize_google(audio_data, language='pl-PL').lower()
            print(text)
            return text
        except sr.UnknownValueError:
            return ''
