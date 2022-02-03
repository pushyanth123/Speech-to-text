from speech_recognition import Recognizer
from speech_recognition import AudioFile
import mimetypes
import re
import subprocess
import random
import sys


supported_file_types = ['wav', 'flac', 'aiff']
supported_conversions = ["mp3", "ogg", "oga"]


class FromAudioFile():
    def __init__(self, input_file_path: str):
        self._input_file_path = input_file_path
        self._audio_encoding = self.get_audio_encoding()

        # Check if the file is in supported formats
        if list(filter(lambda x: re.search(x, self._audio_encoding[1]), supported_file_types)) == []:
            # Write message to stderr
            sys.stdout.write(f"The file {self._input_file_path} is in format. Converting it into wav format")
            self.convert_to_wav()
            self._audio_encoding[1] = "x-wav"

            # Display the messages
            print(
                f"The file {self._input_file_path} is in {self._audio_encoding[1]} format")

    def get_audio_encoding(self) -> str:
        """Function to get the encoding of the "input_file_path"

        Returns:
            str: Type of encoding of the file (Mime type)
        """
        mime_type = mimetypes.guess_type(self._input_file_path)

        # Check if the file is supported (audio and wav or FLAC or aiff)
        if mime_type[0] == None or mime_type[0].split("/")[0] != 'audio':
            raise Exception(
                f"The file {self._input_file_path} is not supported")

        return mime_type[0].split("/")

    def convert_to_wav(self, output_file=None) -> None:
        """Function to convert the given file into wav file

        Returns:
            bool: True if the converstion is successful, False otherwise
        """
        # Check if the file is already in wav format
        if self._audio_encoding[1] == 'wav':
            return

        if output_file != None:
            new_file_name = output_file
        else:
            # Create a new file name (".file_name_some_random_number.wav")
            # Remove the file extension if exists
            new_file_name = re.sub(
                r'\.[^\.]+$', '__{}.wav'.format(random.randint(100000, 999999)), self._input_file_path)

        # Convert the file to wav format
        # Do not output to terminal
        subprocess.run(["ffmpeg", "-loglevel", "0" , "-i", self._input_file_path,
                       new_file_name], stdout=subprocess.DEVNULL)
        self._input_file_path = new_file_name

    def recognize_audio(self, quite=False) -> str:
        """Function to convert audio to text
        """
        # Check if the file is in wav format
        if re.search(r'wav', self._audio_encoding[1]) == None:
            raise Exception(
                f"The file {self._input_file_path} is not in wav format")

        # Recognize the text
        r = Recognizer()
        with AudioFile(self._input_file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            # Check if output file is provided
            if quite == False:
                print("\n\n" + text)

        return text
