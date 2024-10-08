from PyQt5.QtCore import pyqtSignal, QObject
import socketio
import threading

class ChatController(QObject):
    """Контроллер для связи модели и представления."""
    
    # Определение сигнала для получения сообщений/файлов
    message_received = pyqtSignal(str)
    file_received = pyqtSignal(dict)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        
        # Подключение сигналов к слотам для обновления интерфейса
        self.message_received.connect(self.view.append_message)
        self.file_received.connect(self.view.display_file)

        self.view.send_button.clicked.connect(self.send_message)
        self.view.file_button.clicked.connect(self.send_file)
        
        # Socket.IO клиент
        self.sio = socketio.Client()

        # Соединение с сервером в отдельном потоке
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        """Соединение с сервером и привязка событий."""
        self.sio.connect("http://localhost:5000")
        self.sio.on('message', self.receive_message)
        self.sio.on('file', self.receive_file)

    def send_message(self):
        """Отправка текстового сообщения."""
        message = self.view.get_message()
        self.model.add_message(message)
        self.sio.send(message)
        self.view.clear_input()

    def send_file(self):
        """Отправка файла на сервер."""
        file_path = self.view.open_file_dialog()
        if file_path:
            encoded_file = self.model.encode_file(file_path)  # Кодируем файл
            file_name = file_path.split("/")[-1]
            file_extension = file_name.split('.')[-1].lower()
            
            self.sio.emit('file', {'file_name': file_name, 'file_data': encoded_file, 'file_type': file_extension})


    def receive_message(self, msg):
        """Получение сообщения от сервера."""
        self.message_received.emit(msg)  # Эмитируем сигнал, чтобы обновить GUI

    def receive_file(self, file_info):
        """Получение файла от сервера."""
        self.file_received.emit(file_info)  # Эмитируем сигнал для отображения файла
