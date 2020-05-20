from flask_socketio import Namespace, emit


class GameplayNamespace(Namespace):
    def on_connect(self):
        print("connect")

    def on_disconnect(self,):
        print("disconnect")

    def on_emit_method(self, data):
        print("message", data)

    def just_emit(self, data):
        emit("my_response", data)
