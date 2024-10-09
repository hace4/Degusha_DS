import sys
import pyaudio
import socketio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import time

class VoicePlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Player")
        self.setGeometry(100, 100, 300, 200)

        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('voice', self.on_voice)

        self.chunk_size = 8192  # Увеличиваем размер буфера
        self.sample_rate = 44100  # Изменяем на 44100 Гц
        self.channels = 1
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  output=True)

        # Буфер для аудиоданных
        self.audio_buffer = bytearray()
        self.is_playing = False

        # Интерфейс
        self.label = QLabel("Disconnected", self)
        self.connect_button = QPushButton("Connect", self)

        # Верстка
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.connect_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # События на кнопки
        self.connect_button.clicked.connect(self.connect_to_server)

    def connect_to_server(self):
        try:
            self.sio.connect("http://localhost:5000")
        except Exception as e:
            self.label.setText(f"Connection failed: {e}")

    def on_connect(self):
        self.label.setText("Connected")
        self.sio.emit('register', {'public_key': 'dummy'})  # Можно заменить на реальный ключ

    def on_disconnect(self):
        self.label.setText("Disconnected")

    def on_voice(self, data):
        voice_data = data['voice']
        self.audio_buffer.extend(voice_data)

        # Начать воспроизведение, если не воспроизводится в данный момент
        if not self.is_playing:
            self.play_audio()

    def play_audio(self):
        self.is_playing = True
        while self.audio_buffer:
            # Получаем следующий кусок для воспроизведения
            chunk = self.audio_buffer[:self.chunk_size]
            self.audio_buffer = self.audio_buffer[self.chunk_size:]  # Удаляем воспроизведённый кусок
            
            try:
                self.stream.write(bytes(chunk))  # Преобразуем bytearray в bytes
                time.sleep(0.01)  # Небольшая задержка для уменьшения наложений
            except Exception as e:
                print(f"Ошибка воспроизведения аудио: {e}")
                break  # Останавливаем воспроизведение в случае ошибки

        self.is_playing = False  # Сбрасываем статус воспроизведения после завершения

    def closeEvent(self, event):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.sio.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoicePlayer()
    window.show()
    sys.exit(app.exec_())
