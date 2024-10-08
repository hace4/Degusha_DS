from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap  # Импортируем QPixmap
from PyQt5.QtCore import QByteArray

class ChatView(QMainWindow):
    """Представление (GUI) для чата на PyQt."""
    
    def __init__(self):
        super().__init__()
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

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def get_message(self):
        return self.message_input.text()

    def clear_input(self):
        self.message_input.clear()

    def append_message(self, message):
        self.chat_display.append(message)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        return file_path

    def display_file(self, file_info):
        """Отображение полученного файла в интерфейсе."""
        self.chat_display.append(f"Received file: {file_info['file_name']}")
        
        # Если файл является изображением, отображаем его в QTextEdit
        if file_info['file_type'] in ['jpg', 'png', 'gif']:
            # Создаем HTML-код для вставки изображения
            html = f'<img src="data:image/{file_info["file_type"]};base64,{file_info["file_data"]}" width="200" />'
            self.chat_display.append(html)  # Добавляем HTML-код в QTextEdit

