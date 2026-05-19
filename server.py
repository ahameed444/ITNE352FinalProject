import socket
import threading
import json
from meal_api import MealAPI

class RecipeServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5555
        self.cache = self.startup_cache()

    def startup_cache(self):
        print("[SERVER] Initializing reference cache...")
        cats = MealAPI.get_categories()
        areas = MealAPI.get_areas()
        ingr = MealAPI.get_ingredients()
        cache_data = {"categories": cats, "areas": areas, "ingredients": {"meals": ingr.get("meals", [])[:50]}}
        with open("reference.json", "w") as f:
            json.dump(cache_data, f, indent=4)
        return {"categories": cats, "areas": areas, "ingredients": ingr}

    def handle_client(self, conn, addr):
        try:
            username = conn.recv(1024).decode()
            print(f"[NEW CONNECTION] {addr} connected. User: {username}")
            while True:
                data = conn.recv(4096).decode()
                if not data or data == "QUIT":
                    break
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            conn.close()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[LISTENING] Server active...")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    RecipeServer().start()