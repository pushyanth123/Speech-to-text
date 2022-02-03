from speech_recognition import Recognizer
from speech_recognition import Microphone


class FromMicrophone():
    def __init__(self):
        self._recognizer = Recognizer()
        self._microphone = Microphone()
        self._audio = None

    def listen(self, sleep_time=1):
        with self._microphone as source:
            # Adjust the recognizer sensitivity to ambient noise and record audio 
            print(f"Listening starts in {sleep_time} seconds...")
            self._recognizer.adjust_for_ambient_noise(source, duration=sleep_time)
            print("Listening starts...")
            audio = self._recognizer.listen(source)
            print("Listening ends...")
            self._audio = audio

    def recognize_audio(self, quite=False):
        if self._audio is None:
            raise Exception("Audio is not recorded yet.")
        try:
            text = self._recognizer.recognize_google(self._audio, show_all=quite)
            if quite == True:
                print(text)

            return text
        except Exception as e:
            print(e)
            exit(1)