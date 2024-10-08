import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from websocket import create_connection
import threading

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

        self.ws = create_connection("ws://localhost:5000")
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.message_input.text()
        self.ws.send(message)
        self.message_input.clear()

    def receive_messages(self):
        while True:
            message = self.ws.recv()
            self.chat_display.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())