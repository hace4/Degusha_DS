import base64

class ChatModel:
    """Модель данных для чата."""
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
    
    def encode_file(self, file_path):
        """Кодирует файл в base64 для передачи."""
        with open(file_path, 'rb') as file:
            file_data = file.read()
        return base64.b64encode(file_data).decode('utf-8')
    
    def decode_file(self, encoded_file, file_name):
        """Декодирует файл из base64 и сохраняет на диск."""
        file_data = base64.b64decode(encoded_file)
        with open(file_name, 'wb') as file:
            file.write(file_data)
        return file_name
