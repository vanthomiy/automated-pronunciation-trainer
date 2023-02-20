import glob

import io
import pyaudio

from pydub import AudioSegment


class NoiseAdder:
    def __init__(self, filename, chunk_size=1024, sample_format=pyaudio.paInt16, channels=2, sample_rate=44100):
        self.filename = filename
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.channels = channels
        self.sample_rate = sample_rate
        self.noises = self.load_noises()
        self.selected_noise = "None"
        self.p = pyaudio.PyAudio()

    import struct
    def save_file(self, byte_array):
        """
        Save byte array as mp3 file
        :param byte_array:
        :return:
        """
        # Assume the audio/webm data is in a byte array named "webm_data"
        webm_io = io.BytesIO(byte_array)

        # Load the audio/webm data as an AudioSegment object
        audio_segment = AudioSegment.from_file(webm_io, format="webm")

        # Convert the audio segment to mp3 format
        mp3_data = audio_segment.export(format="mp3").read()

        # Save the mp3 data to a file
        with open("output.mp3", "wb") as f:
            f.write(mp3_data)

    def get_noise_array(self, other_path=None) -> bytearray:
        """
        Returns the selected noise
        """
        if other_path is not None:
            audio_file = other_path
        else:
            audio_file = f"noise/{self.selected_noise}.mp3"

        # Open the ..mp3 file as byte array
        with open(audio_file, "rb") as f:
            byte_array = bytearray(f.read())
            return byte_array

    def get_noise(self):
        """
        Returns the selected noise
        """
        return self.noises[self.selected_noise]

    def load_noises(self) -> dict:
        """
        Loads all noise files from the noise folder
        :return:
        """
        noises = {}
        # get all noise files
        noise_files = glob.glob("noise/*.mp3")
        for noise_file in noise_files:
            # open noise file using pydub
            wf = AudioSegment.from_file(noise_file, format="mp3")
            # add noise to noises (key is filename without ..mp3)
            noises[noise_file.split("\\")[1].split(".")[0]] = wf

        noises["None"] = None

        return noises

    def add_noise(self):
        """
        Adds noise to the recorded audio file
        :return:
        """

        if self.selected_noise == "None":
            return None

        noise_file = f"./noise/{self.selected_noise}.mp3"
        sound1 = AudioSegment.from_file(noise_file, format="mp3")
        sound2 = AudioSegment.from_file("output.mp3", format="mp3")

        # region  Crop sound1 to the length of sound2 if sound1 is longer
        if len(sound1) > len(sound2):
            sound1 = sound1[:len(sound2)]
        else:
            # increase length of sound1 to the length of sound2 if sound2 is longer
            sound1 = sound1 * (len(sound2) // len(sound1) + 1)
        # endregion
        # Adjust volume of sound1 and sound2
        sound1 = sound1 + 6  # boost volume by 6dB
        sound2 = sound2 - 3  # reduce volume by 3dB
        # Add sound1 and sound2 together
        combined = sound1.overlay(sound2)
        # Export combined sound as mp3 file
        combined.export("output.mp3", format="mp3")
