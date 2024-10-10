# server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Словарь для хранения клиентов и их имен
clients = {}

@app.route('/')
def index():
    return "Combined Chat and Voice server is running."

@socketio.on('connect')
def handle_connect():
    user_id = request.sid  # Используем идентификатор сессии в качестве имени пользователя
    clients[user_id] = {'public_key': None}  # Добавляем клиента
    naming = f'User-{user_id}'
    print(f"Client {user_id} connected")
    emit('set_name', {'name': naming})  # Отправляем имя клиенту

@socketio.on('register')
def handle_register(data):
    user_id = request.sid
    clients[user_id]['public_key'] = data['public_key']
    print(f"Client {user_id} registered with public key: {data['public_key']}")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    clients.pop(user_id, None)
    print(f"Client {user_id} disconnected")

# Обработчик сообщений
@socketio.on('message')
def handle_message(msg):
    user_id = request.sid
    msg["name"] = clients[user_id]['public_key'] or f'User-{user_id}'  # Используем публичный ключ или имя по умолчанию
    emit('message', msg, broadcast=True)  # Добавляем имя к сообщению

# Обработчик голосовых данных
@socketio.on('voice')
def handle_voice(data):
    client_name = clients.get(request.sid, {'public_key': 'Anonymous'})['public_key']
    print(f"Received voice data from {client_name}")
    # Передаем голосовые данные другим клиентам с добавлением имени
    for client in clients:
        if client != request.sid:
            emit('voice', {'name': client_name, 'voice': data['voice']}, room=client)

# Обработчик файлов
@socketio.on('file')
def handle_file(data):
    client_name = clients.get(request.sid, {'public_key': 'Anonymous'})['public_key']
    file_name = data['file_name']
    file_data = data['file_data']
    file_type = data['file_type']

    print(f"Received file from {client_name}: {file_name}")
    emit('file', {'name': client_name, 'file_name': file_name, 'file_data': file_data, 'file_type': file_type}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
