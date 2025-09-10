import speech_recognition as sr


class Transcriber:
    def __init__(self):
        self.model = sr.Recognizer()

    def transcribe_file(self, file_path: str):
        """Turns audio file to text and returns the text"""
        with sr.AudioFile(file_path) as source:
            audio_data = self.model.record(source)

        try:
            text = self.model.recognize_google(audio_data)
            return text

        except sr.UnknownValueError:
            raise Exception("Could not understand audio from file.")
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")

