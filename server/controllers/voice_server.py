# server/voice_server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

clients = []

@app.route('/')
def index():
    return "Voice chat server is running."

@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(f"Client {request.sid} connected")

@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    print(f"Client {request.sid} disconnected")

@socketio.on('voice')
def handle_voice(data):
    for client in clients:
        if client != request.sid:
            emit('voice', data, room=client)

if __name__ == '__main__':
    socketio.run(app, debug=True)
