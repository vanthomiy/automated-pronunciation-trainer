import glob

import pyaudio
import wave

import threading
from pydub import AudioSegment


class SoundRecorder:
    def __init__(self, filename, chunk_size=1024, sample_format=pyaudio.paInt16, channels=2, sample_rate=44100):
        self.filename = filename
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.channels = channels
        self.sample_rate = sample_rate
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.is_recording = False
        self.play = False
        self.stream = None
        self.t = None

    def start(self) -> bool:
        """
        Starts the recording by opening the audio stream and starting a thread
        :return:
        """
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  frames_per_buffer=self.chunk_size,
                                  input=True)
        self.is_recording = True
        self.t = threading.Thread(target=self.record)
        self.t.start()

        print("recording started")
        return True

    def stop(self):
        """
        Stops the recording and saves the audio data to a file
        :return:
        """
        self.is_recording = False

        self.t.join()

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("recording stopped")

    def record(self):
        """
        Records audio data from the microphone and stores it in the frames list
        :return:
        """
        while self.is_recording:
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)


class SoundPlayer:
    def __init__(self, sound, chunk_size=1024, sample_format=pyaudio.paInt16, channels=2, sample_rate=44100):
        self.audio = sound
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.channels = channels
        self.sample_rate = sample_rate
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.play = False
        self.t = None

    def start(self) -> bool:
        """
        Plays a noise on the speakers
        :param audio:
        :param noise_name:
        :return:
        """
        self.t = threading.Thread(target=self.play_sound)
        self.t.start()
        return True

    def play_sound(self):
        """
        Plays the selected noise on the speakers
        :return:
        """
        wf = self.audio
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)
        data = wf.readframes(self.chunk_size)
        while data != b'' and self.play:
            stream.write(data)
            data = wf.readframes(self.chunk_size)
        stream.stop_stream()
        stream.close()
        # the file is blocked
        wf.close()
        self.p.terminate()


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
        noise_files = glob.glob("noise/*.wav")
        for noise_file in noise_files:
            wf = wave.open(noise_file, 'rb')
            # add noise to noises (key is filename without .wav)
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

        sound1 = AudioSegment.from_file(f"./noise/{self.selected_noise}.wav", format="wav")
        sound2 = AudioSegment.from_file(f"./output.wav", format="wav")
        #region  Crop sound1 to the length of sound2 if sound1 is longer
        if len(sound1) > len(sound2):
            sound1 = sound1[:len(sound2)]
        else:
            # increase length of sound1 to the length of sound2 if sound2 is longer
            sound1 = sound1 * (len(sound2) // len(sound1) + 1)
        #endregion
        # Adjust volume of sound1 and sound2
        sound1 = sound1 + 6  # boost volume by 6dB
        sound2 = sound2 - 3  # reduce volume by 3dB
        # Add sound1 and sound2 together
        combined = sound1.overlay(sound2)
        # Export combined sound as wav file
        combined.export("./output.wav", format="wav")

        return combined
