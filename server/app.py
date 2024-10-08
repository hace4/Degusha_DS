from flask import Flask
from controllers.chat_server import ChatServer

# Создаем экземпляр Flask
app = Flask(__name__)

# Передаем его в ChatServer
chat_server = ChatServer(app)

if __name__ == "__main__":
    chat_server.run()
