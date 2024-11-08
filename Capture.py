import pyaudio
import wave
import numpy as np

import pygame
import Utility

from Utility import SoundManager

pygame.init()

# Sound effects
SOUND_EFFECTS = Utility.SOUND_EFFECTS

def getconf() -> dict:
    config = {
        "CHUNK": 1024,
        "FORMAT": pyaudio.paInt32,
        "CHANNELS": 2,
        "RATE": 44100,
        "RECORD_SECONDS": 15,
        "WAVE_OUTPUT_FILENAME": "Resources/Audio_Recordings/speech.wav"
    }

    return config


class Capture:

    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()
        self.config = getconf()
        self.frames = []
        self.isPipeOpen = True
        self.isStreamRunning = True
        self.permitCollect = False
        self.recSecs = 5
        self.volume = 15
        self.permitRun = False
        self.stream = self.p.open(format=self.config["FORMAT"], channels=self.config["CHANNELS"],
                                  rate=self.config["RATE"], input=True, frames_per_buffer=self.config["CHUNK"])

    def adjust_time(self, value) -> None:

        self.recSecs = value

    def adjust_volume(self, value) -> None:

        self.volume = value

    def adjust_volume(self, data):
        # Convert binary data to a numpy array
        audio_data = np.frombuffer(data, dtype=np.int32)
        # Apply volume adjustment
        audio_data = (audio_data * self.volume).astype(np.int32)
        # Convert back to binary data
        return audio_data.tobytes()

    def get_audio(self) -> None:
        SoundManager.play(SOUND_EFFECTS['mic_on'])
        if not self.isStreamRunning:

            if self.isPipeOpen:
                self.stream = self.p.open(format=self.config["FORMAT"], channels=self.config["CHANNELS"],
                                          rate=self.config["RATE"], input=True, frames_per_buffer=self.config["CHUNK"])
                self.isPipeOpen = True
            else:
                self.p = pyaudio.PyAudio()
                self.stream = self.p.open(format=self.config["FORMAT"], channels=self.config["CHANNELS"],
                                          rate=self.config["RATE"], input=True, frames_per_buffer=self.config["CHUNK"])
                self.isPipeOpen = True
                self.isStreamRunning = True

        elif not self.isPipeOpen:

            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.config["FORMAT"], channels=self.config["CHANNELS"],
                                      rate=self.config["RATE"], input=True, frames_per_buffer=self.config["CHUNK"])
            self.isPipeOpen = True
            self.isStreamRunning = True

        for i in range(0, int(self.config["RATE"] / self.config["CHUNK"] * self.recSecs)):
            data = self.stream.read(self.config["CHUNK"])
            self.frames.append(data)

        self.write_audio()

    def stop_audio(self) -> None:

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self.isPipeOpen = False
        self.isStreamRunning = False

    def write_audio(self) -> None:

        try:
            wf = wave.open(self.config["WAVE_OUTPUT_FILENAME"], 'wb')
            frms = []
            for x in self.frames:
                amp = self.adjust_volume(x)
                frms.append(amp)
            wf.setnchannels(self.config["CHANNELS"])
            wf.setsampwidth(self.p.get_sample_size(self.config["FORMAT"]))
            wf.setframerate(self.config["RATE"])
            wf.writeframes(b''.join(frms))
            wf.close()
            self.stop_audio()
        except IOError as ie:

            print(f"Unknown error while writing the audio.\n{ie}")

# c = Capture()
# c.adjust_time(10)
# c.get_audio()