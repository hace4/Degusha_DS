# client/views/call_view.py

from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel

class CallView(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Call")

        self.layout = QVBoxLayout()

        self.call_label = QLabel("Calling...")
        self.layout.addWidget(self.call_label)

        self.end_call_button = QPushButton("End Call")
        self.end_call_button.clicked.connect(self.end_call)
        self.layout.addWidget(self.end_call_button)

        self.setLayout(self.layout)

    def end_call(self):
        self.close()
