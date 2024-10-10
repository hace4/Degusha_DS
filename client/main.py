# main.py
import sys
from PyQt5.QtWidgets import QApplication
from models.AudioModel import AudioModel
from controllers.AudioController import AudioController
from controllers.ChatController import ChatController
from views.ChatView import ChatView

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем модель, контроллеры и представление
    audio_model = AudioModel()
    audio_controller = AudioController(audio_model)
    chat_view = ChatView()
    chat_controller = ChatController(audio_controller, chat_view)

    # Устанавливаем контроллер для представления
    chat_view.set_controller(chat_controller)

    # Показываем представление
    chat_view.show()

    # Запускаем приложение
    sys.exit(app.exec_())
