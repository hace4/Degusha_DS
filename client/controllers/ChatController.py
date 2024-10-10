# chat_controller.py
from PyQt5.QtCore import QObject, pyqtSignal

class ChatController(QObject):
    message_received = pyqtSignal(dict)
    file_received = pyqtSignal(dict)

    def __init__(self, audio_controller, view):
        super().__init__()
        self.audio_controller = audio_controller
        self.view = view
        self.user_name = ""

    def connect(self, server_url):
        return self.audio_controller.connect(server_url)

    def start_recording(self):
        self.audio_controller.start_recording()

    def stop_recording(self):
        self.audio_controller.stop_recording()

    def record_and_send(self):
        self.audio_controller.record_and_send()

    def send_message(self):
        message = self.view.get_message()
        if message:
            self.view.clear_input()
            self.message_received.emit({"message": message, "name": self.user_name})

    def send_file(self):
        file_path = self.view.open_file_dialog()
        if file_path:
            # Логика для отправки файла на сервер
            pass

    def receive_message(self, msg):
        self.message_received.emit(msg)

    def receive_file(self, file_info):
        self.file_received.emit(file_info)

    def on_set_name(self, data):
        """Обработка события получения имени от сервера."""
        self.user_name = data['name']
        print(f"Your assigned name is: {self.user_name}")
