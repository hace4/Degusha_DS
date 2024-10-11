# audio_controller.py
import socketio

class AudioController:
    def __init__(self, model):
        self.model = model
        self.sio = socketio.Client()
        self.is_recording = False
        self.UserName = ''
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('voice', self.on_voice)
        self.sio.on('set_name', self.on_set_name)

    def connect(self, server_url):
        try:
            self.sio.connect(server_url)
        except Exception as e:
            return f"Connection failed: {e}"

    def disconnect(self):
        self.sio.disconnect()

    def start_recording(self):
        """Начать запись звука."""
        self.is_recording = True

    def stop_recording(self):
        """Остановить запись звука."""
        self.is_recording = False

    def record_and_send(self):
        """Запись и отправка звука на сервер."""
        if self.is_recording:
            voice_data = self.model.record_audio()  # Метод записи звука из модели
            if voice_data:
                self.sio.emit('voice', {'voice': voice_data})

    def on_connect(self):
        print("Connected to audio server")

    def on_disconnect(self):
        print("Disconnected from audio server")

    def on_voice(self, data):
        voice_data = data['voice']
        self.model.play_audio(voice_data)  # Метод воспроизведения звука из модели
        
    def on_set_name(self, data):
        """Обработка события получения имени от сервера."""
        self.UserName = data['name']
        print(f"Your assigned name is: {self.UserName}")
