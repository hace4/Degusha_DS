import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
import socketio

class ChatClient(QMainWindow):
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
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Создаем Socket.IO клиент
        self.sio = socketio.Client()

        # Подключаем обработчики событий
        self.sio.on('message', self.receive_message)

        # Подключаемся к серверу
        self.sio.connect("http://localhost:5000")

    def send_message(self):
        message = self.message_input.text()
        self.sio.send(message)  # Отправляем сообщение через Socket.IO
        self.message_input.clear()

    def receive_message(self, msg):
        # Обработка получения сообщения от сервера
        self.chat_display.append(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())
