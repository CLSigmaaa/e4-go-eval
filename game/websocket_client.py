import websocket
import threading
import json

class WebSocketClient:
    def __init__(self, game, url):
        self.game = game
        self.url = url
        self.ws = None
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(self.url, 
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()
        
    def on_open(self, ws):
        print("Connection opened")

    def on_message(self, ws, message):
        pass
        
    def send(self, data):
        self.ws.send(json.dumps(data))

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws):
        print("Connection closed")

if __name__ == "__main__":
    client = WebSocketClient("ws://localhost:8080/ws")