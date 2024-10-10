import pyaudio
import numpy as np
import noisereduce as nr
import webrtcvad
from scipy.signal import butter, lfilter

class AudioModel:
    def __init__(self):
        # Настройки аудио
        self.chunk_size = 320
        self.sample_rate = 16000
        self.channels = 1
        self.p = pyaudio.PyAudio()

        # Инициализация потока для записи
        self.stream_input = self.p.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.sample_rate,
                                        input=True,
                                        frames_per_buffer=self.chunk_size)

        # Инициализация потока для воспроизведения
        self.stream_output = self.p.open(format=pyaudio.paInt16,
                                         channels=self.channels,
                                         rate=self.sample_rate,
                                         output=True)

        # Инициализация VAD
        self.vad = webrtcvad.Vad(1)

        # Буфер для воспроизведения
        self.audio_buffer = bytearray()
        self.is_playing = False

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut):
        b, a = self.butter_bandpass(lowcut, highcut, self.sample_rate)
        return lfilter(b, a, data)

    def record_audio(self):
        voice_data = self.stream_input.read(self.chunk_size, exception_on_overflow=False)
        voice_array = np.frombuffer(voice_data, dtype=np.int16)

        # Шумоподавление
        voice_array = nr.reduce_noise(y=voice_array, sr=self.sample_rate)

        # Применение фильтра
        voice_array = self.bandpass_filter(voice_array, 150.0, 3900.0)

        # Использование VAD для определения речи
        if self.vad.is_speech(voice_data, self.sample_rate):
            return voice_data  # Возвращаем только если речь обнаружена
        return None

    def play_audio(self, voice_data):
        self.audio_buffer.extend(voice_data)

        if not self.is_playing:
            self.is_playing = True
            while self.audio_buffer:
                chunk = self.audio_buffer[:self.chunk_size]
                self.audio_buffer = self.audio_buffer[self.chunk_size:]
                self.stream_output.write(bytes(chunk))
            self.is_playing = False

    def close(self):
        self.stream_input.stop_stream()
        self.stream_input.close()
        self.stream_output.stop_stream()
        self.stream_output.close()
        self.p.terminate()
