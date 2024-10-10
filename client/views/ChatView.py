# chat_view.py
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PyQt5.QtCore import QTimer

class ChatView(QMainWindow):
    """Представление (GUI) для чата на PyQt."""
    
    def __init__(self):
        super().__init__()
        self.controller = None  # Изначально контроллер будет None
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.message_input = QLineEdit()
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.layout.addWidget(self.send_button)
        
        self.file_button = QPushButton("Send File")
        self.layout.addWidget(self.file_button)

        self.label = QLabel("Disconnected", self)
        self.layout.addWidget(self.label)
        
        self.connect_button = QPushButton("Connect")
        self.layout.addWidget(self.connect_button)
        
        self.start_record_button = QPushButton("Start Recording")
        self.layout.addWidget(self.start_record_button)
        
        self.stop_record_button = QPushButton("Stop Recording")
        self.layout.addWidget(self.stop_record_button)
        
        self.connect_button.clicked.connect(self.connect_to_server)
        self.start_record_button.clicked.connect(self.start_recording)
        self.stop_record_button.clicked.connect(self.stop_recording)

        # Таймер для записи аудио
        self.timer = QTimer()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def set_controller(self, controller):
        """Метод для установки контроллера после его создания."""
        self.controller = controller
        # Подключаем сигналы контроллера к слотам
        self.controller.message_received.connect(self.append_message)
        self.controller.file_received.connect(self.display_file)
        self.send_button.clicked.connect(self.controller.send_message)
        self.file_button.clicked.connect(self.controller.send_file)
        
        # Подключаем метод к таймеру после установки контроллера
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
        self.label.setText("Stopped Recording")
        self.controller.stop_recording()
        self.timer.stop()

    def append_message(self, msg):
        """Добавить сообщение в текстовое поле."""
        self.chat_display.append(f"{msg['name']}: {msg['message']}")

    def display_file(self, file_info):
        """Логика для отображения файлов в чате."""
        self.chat_display.append(f"File received from {file_info['name']}: {file_info['file_name']}")

    def get_message(self):
        """Получить сообщение из поля ввода."""
        return self.message_input.text()

    def clear_input(self):
        """Очистить поле ввода."""
        self.message_input.clear()

    def open_file_dialog(self):
        """Открыть диалог для выбора файла и вернуть путь к файлу."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        return file_path
