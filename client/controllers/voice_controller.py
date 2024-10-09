import sys
import pyaudio
import socketio
import numpy as np
import noisereduce as nr
import webrtcvad
from scipy.signal import butter, lfilter
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer

class VoiceRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Recorder")
        self.setGeometry(100, 100, 300, 200)

        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)

        # Настройки аудио
        self.chunk_size = 320  # Установите размер чанка
        self.sample_rate = 16000
        self.channels = 1
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk_size)

        self.vad = webrtcvad.Vad(1)  # Установите на более агрессивный режим (0-3)
        self.timer = QTimer()
        self.timer.timeout.connect(self.record_audio)

        # Интерфейс
        self.label = QLabel("Disconnected", self)
        self.connect_button = QPushButton("Connect", self)
        self.start_record_button = QPushButton("Start Recording", self)
        self.stop_record_button = QPushButton("Stop Recording", self)

        # Верстка
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.start_record_button)
        layout.addWidget(self.stop_record_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # События на кнопки
        self.connect_button.clicked.connect(self.connect_to_server)
        self.start_record_button.clicked.connect(self.start_recording)
        self.stop_record_button.clicked.connect(self.stop_recording)

    def connect_to_server(self):
        try:
            self.sio.connect("http://localhost:5000")
        except Exception as e:
            self.label.setText(f"Connection failed: {e}")

    def on_connect(self):
        self.label.setText("Connected")
        self.sio.emit('register', {'public_key': 'dummy'})

    def on_disconnect(self):
        self.label.setText("Disconnected")

    def start_recording(self):
        self.label.setText("Recording...")
        self.timer.start(10)

    def stop_recording(self):
        self.label.setText("Stopped")
        self.timer.stop()

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut):
        b, a = self.butter_bandpass(lowcut, highcut, self.sample_rate)
        # Здесь была допущена ошибка, отсутствовала фильтрация данных
        filtered_data = lfilter(b, a, data)
        return filtered_data
    
    def record_audio(self):
        try:
            # Чтение аудиоданных из микрофона
            voice_data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            voice_array = np.frombuffer(voice_data, dtype=np.int16)

            # Шумоподавление
            voice_array = nr.reduce_noise(y=voice_array, sr=self.sample_rate)

            # Применение фильтра
            voice_array = self.bandpass_filter(voice_array, 150.0, 3900.0)

            # Использование VAD (Voice Activity Detection)
            is_speech = self.vad.is_speech(voice_data, self.sample_rate)

            # Убедитесь, что записываем только речь
            if is_speech:
                # Отправляем звук на сервер в виде bytes
                self.sio.emit('voice', {'voice': voice_data})  # Передаем voice_data напрямую

        except Exception as e:
            print(f"Error recording audio: {e}")

    def closeEvent(self, event):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.sio.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceRecorder()
    window.show()
    sys.exit(app.exec_())
