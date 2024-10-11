from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer

class AudioView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Voice Client")
        self.setGeometry(100, 100, 300, 200)

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

        # Таймер для записи аудио
        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.record_and_send)

    def connect_to_server(self):
        server_url = "http://localhost:5000"
        error = self.controller.connect(server_url)
        if error:
            self.label.setText(error)
        else:
            self.label.setText("Connected")

    def start_recording(self):
        self.label.setText("Recording...")
        self.controller.start_recording()
        self.timer.start(10)

    def stop_recording(self):
        self.label.setText("Stopped")
        self.controller.stop_recording()
        self.timer.stop()

    def closeEvent(self, event):
        self.controller.disconnect()
        self.controller.model.close()
        event.accept()
