import sys
import pyaudio
import socketio
import numpy as np
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
        self.chunk_size = 8192  # Увеличиваем размер буфера
        self.sample_rate = 44100  # Изменяем на 44100 Гц
        self.channels = 1
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk_size)

        # Таймер для записи
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
            print(f"Connection error: {e}")

    def on_connect(self):
        self.label.setText("Connected")
        self.sio.emit('register', {'public_key': 'dummy'})
        print("Connected to server")

    def on_disconnect(self):
        self.label.setText("Disconnected")
        print("Disconnected from server")

    def start_recording(self):
        self.label.setText("Recording...")
        self.timer.start(10)

    def stop_recording(self):
        self.label.setText("Stopped")
        self.timer.stop()

    def record_audio(self):
        try:
            voice_data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            voice_array = np.frombuffer(voice_data, dtype=np.int16)

            # Отправляем звук на сервер (без обработки)
            self.sio.emit('voice', {'voice': voice_data})  # Отправляем необработанный звук
            print("Sent audio data")
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
