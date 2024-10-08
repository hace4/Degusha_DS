import sys
from PyQt5.QtWidgets import QApplication
from models.chat_model import ChatModel
from views.chat_view import ChatView
from controllers.chat_controller import ChatController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = ChatModel()
    view = ChatView()
    controller = ChatController(model, view)

    view.show()
    sys.exit(app.exec_())
