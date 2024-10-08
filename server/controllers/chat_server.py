from flask_socketio import SocketIO, emit

class ChatServer:
    """Сервер для обработки сообщений и файлов."""

    def __init__(self, app):
        self.app = app  # Сохраняем ссылку на приложение Flask
        self.socketio = SocketIO(self.app)
        self.register_routes()
        self.register_socket_events()

    def register_routes(self):
        @self.app.route('/')
        def index():
            return "Chat server is running."

    def register_socket_events(self):
        @self.socketio.on('message')
        def handle_message(msg):
            print(f"Received message: {msg}")
            emit('message', msg, broadcast=True)

        @self.socketio.on('file')
        def handle_file(data):
            file_name = data['file_name']
            file_data = data['file_data']
            file_type = data['file_type']

            print(f"Received file: {file_name}")
            emit('file', {'file_name': file_name, 'file_data': file_data, 'file_type': file_type}, broadcast=True)

    def run(self):
        self.socketio.run(self.app, debug=True)
