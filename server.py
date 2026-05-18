import socket

class RecipeServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5555

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[LISTENING] Server active on {self.host}:{self.port}...")

if __name__ == "__main__":
    RecipeServer().start()